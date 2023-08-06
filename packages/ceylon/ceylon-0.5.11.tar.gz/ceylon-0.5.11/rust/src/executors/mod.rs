use anyhow::Result;
use paris::error;
// pyO3 module
use pyo3::prelude::*;

pub async fn execute_event_handler(
    handler: Py<PyAny>,
    arguments: Py<PyAny>,
) -> Result<()> {
    // info!("Startup event handler async");
    match Python::with_gil(|py| {
        let asyncio = py.import("asyncio")?;
        let event_loop = asyncio.call_method0("new_event_loop")?;
        // Set the event loop
        asyncio.call_method1("set_event_loop", (event_loop,))?;
        match handler.as_ref(py).call1((arguments, )) {
            Ok(re) => {
                match event_loop.call_method1("run_until_complete", (re, )) {
                    Ok(_) => {
                        // info!("Startup event handler async done {}",_re);
                        Ok(())
                    }
                    Err(e) => {
                        error!("Error: {}", e);
                        Ok(())
                    }
                }
            }
            Err(e) => {
                error!("Startup event handler async error: {}", e);
                Err(e)
            }
        }
    }) {
        Ok(_) => Ok(()),
        Err(e) => {
            error!("Startup event handler async error: {}", e);
            Ok(())
        }
    }
}