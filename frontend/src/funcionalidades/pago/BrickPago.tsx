import { Wallet } from "@mercadopago/sdk-react"
import { Spinner } from "@/componentes/ui/Spinner"
import { inicializarMP, MP_CONFIGURADO } from "@/lib/mercadopago"

inicializarMP()

interface Props {
  preferenciaId: string
  ordenId: number
}

export function BrickPago({ preferenciaId, ordenId }: Props) {
  if (!MP_CONFIGURADO) {
    return (
      <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-5 text-center text-sm text-yellow-800">
        <p className="font-semibold">MercadoPago no configurado</p>
        <p className="mt-1 text-xs">
          Definí{" "}
          <code className="rounded bg-yellow-100 px-1">
            VITE_CLAVE_PUBLICA_MP
          </code>{" "}
          en tu <code className="rounded bg-yellow-100 px-1">.env</code>.
        </p>
        <p className="mt-3 text-xs text-yellow-700">
          Orden #{ordenId} creada — preferencia:{" "}
          <span className="font-mono">{preferenciaId}</span>
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold">3. Completá el pago</h2>
      <Wallet
        initialization={{ preferenceId: preferenciaId, redirectMode: "self" }}
        onReady={() => undefined}
        onError={(err) => console.error("MP Brick error:", err)}
      />
    </div>
  )
}

export function BrickPagoCargando() {
  return (
    <div className="flex items-center justify-center rounded-xl border border-gray-100 bg-white p-10 shadow-sm">
      <Spinner />
    </div>
  )
}
