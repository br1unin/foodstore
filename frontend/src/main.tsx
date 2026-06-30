import React from "react"
import ReactDOM from "react-dom/client"
import { QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import { App } from "@/App"
import { clienteConsultas } from "@/lib/clienteConsultas"
import { CajonCarrito } from "@/funcionalidades/carrito/CajonCarrito"
import "@/index.css"

ReactDOM.createRoot(document.getElementById("raiz")!).render(
  <React.StrictMode>
    <QueryClientProvider client={clienteConsultas}>
      <App />
      <CajonCarrito />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>,
)
