use pyo3::{
    exceptions::PyRuntimeError,
    prelude::*,
    types::{PyBool, PyDict, PyList, PySequence},
};
use std::{collections::HashMap, sync::Arc};
use tera::{Context, Tera};

#[pyclass]
struct TeraTemplates {
    engine: Arc<Tera>,
    dirs: Vec<String>,
    app_dirs: bool,
}

#[pymethods]
impl TeraTemplates {
    #[new]
    fn new(params: &PyDict) -> PyResult<TeraTemplates> {
        let dirs = Python::with_gil(|py| {
            params
                .get_item("DIRS")
                .unwrap_or(PyList::new(py, Vec::<String>::new()))
                .extract()
        })?;

        let app_dirs = Python::with_gil(|py| {
            params
                .get_item("APP_DIRS")
                .unwrap_or(PyBool::new(py, true))
                .extract()
        })?;

        match Tera::new("templates/**/*.html") {
            Ok(engine) => Ok(TeraTemplates {
                engine: Arc::new(engine),
                dirs,
                app_dirs,
            }),
            Err(err) => Err(DjangoTeraError::new_err(err.to_string())),
        }
    }

    fn get_template(&self, template_name: String) -> Template {
        Template {
            engine: self.engine.clone(),
            template_name,
        }
    }
}

#[pyclass]
struct Template {
    engine: Arc<Tera>,
    template_name: String,
}

#[pymethods]
impl Template {
    fn render(&self, context: &PyDict, request: &PyAny) -> PyResult<String> {
        let mut tera_context = Context::new();

        for (key, value) in context.iter() {
            let key = key.extract::<String>()?;
            let context_value = value.extract::<ContextValue>()?;
            tera_context.insert(&key, &context_value);
        }

        if !request.is_none() {
            let mut request_ctx = HashMap::new();

            const ATTRS: [&str; 11] = [
                "GET",
                "POST",
                "COOKIES",
                "FILES",
                "path",
                "path_info",
                "method",
                "content_type",
                "content_params",
                "scheme",
                "encoding",
                // TODO: META, headers, ...
            ];

            for attr in ATTRS {
                let value = request.getattr(attr)?;
                if !value.is_none() {
                    request_ctx.insert(
                        attr.to_string(),
                        request.getattr(attr)?.extract::<ContextValue>()?,
                    );
                }
            }

            let resolver_match = request.getattr("resolver_match")?;
            if !resolver_match.is_none() {
                let mut resolver_match_context = HashMap::new();

                for attr in [
                    "args",
                    "kwargs",
                    "captured_kwargs",
                    "extra_kwargs",
                    "url_name",
                    "route",
                    "app_name",
                    "app_names",
                    "namespace",
                    "view_name",
                    // TODO: tried
                ] {
                    let value = resolver_match.getattr(attr)?;
                    if !value.is_none() {
                        resolver_match_context
                            .insert(attr.to_string(), value.extract::<ContextValue>()?);
                    }
                }

                request_ctx.insert(
                    "resolver_match".to_string(),
                    ContextValue::Dict(resolver_match_context),
                );
            }

            tera_context.insert("request", &request_ctx);
        }

        match self.engine.render(&self.template_name, &tera_context) {
            Ok(rendered) => Ok(rendered),
            Err(err) => Err(DjangoTeraError::new_err(format!("{err:?}"))),
        }
    }
}

#[derive(FromPyObject, serde::Serialize)]
#[serde(untagged)]
enum ContextValue {
    #[pyo3(transparent, annotation = "str")]
    String(String),
    #[pyo3(transparent, annotation = "float")]
    Float(f64),
    #[pyo3(transparent, annotation = "int")]
    Int(i64),
    #[pyo3(transparent, annotation = "list")]
    List(Vec<ContextValue>),
    #[pyo3(transparent, annotation = "dict")]
    Dict(HashMap<String, ContextValue>),
}

/// A Python module implemented in Rust.
#[pymodule]
fn django_tera(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<TeraTemplates>()?;
    m.add_class::<Template>()?;
    Ok(())
}

pyo3::create_exception!(django_tera, DjangoTeraError, PyRuntimeError);
