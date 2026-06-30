import { useEffect } from "react"
import { Link, useSearchParams } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"
import { clavesConsulta } from "@/lib/clavesConsulta"
import { carritoStore } from "@/almacenes/carritoStore"

export function PaginaPagoExito() {
  const [params] = useSearchParams()
  const cliente = useQueryClient()
  const limpiarCarrito = carritoStore((s) => s.vaciarCarrito)

  const ordenId = params.get("external_reference")
  const paymentId = params.get("payment_id")

  useEffect(() => {
    limpiarCarrito()
    cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.misOrdenes() })
    if (ordenId) {
      cliente.invalidateQueries({
        queryKey: clavesConsulta.ordenes.detalle(Number(ordenId)),
      })
    }
  }, [limpiarCarrito, cliente, ordenId])

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6 text-center">
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-green-100 text-4xl">
        ✓
      </div>
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-green-700">¡Pago aprobado!</h1>
        <p className="text-gray-500">
          Tu pedido fue confirmado y está siendo procesado.
        </p>
        {paymentId && (
          <p className="text-xs text-gray-400">
            Referencia de pago: {paymentId}
          </p>
        )}
      </div>
      <div className="flex gap-3">
        {ordenId && (
          <Link
            to={`/mis-ordenes/${ordenId}`}
            className="rounded-xl bg-primario-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-primario-700"
          >
            Ver mi pedido
          </Link>
        )}
        <Link
          to="/mis-ordenes"
          className="rounded-xl border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50"
        >
          Mis órdenes
        </Link>
      </div>
    </div>
  )
}
