use pyo3::prelude::*;
use pyo3::types::PyBytes;
use scenewriter::fountain_to_html as fountain_to_html_;
use scenewriter::fountain_to_pdf as fountain_to_pdf_;
use scenewriter::pdf::PaperSize;

// Convert fountain format to html
#[pyfunction]
fn fountain_to_html(input: &str) -> PyResult<String> {
    Ok(fountain_to_html_(input))
}

// Convert fountain format to pdf
#[pyfunction]
fn fountain_to_pdf(py: Python, input: &str /*, paper_size: PaperSize */) -> PyObject {
    let bytes = fountain_to_pdf_(input, PaperSize::A4);
    PyBytes::new(py, &bytes).into()
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyscenewriter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fountain_to_html, m)?)?;
    m.add_function(wrap_pyfunction!(fountain_to_pdf, m)?)?;
    Ok(())
}
