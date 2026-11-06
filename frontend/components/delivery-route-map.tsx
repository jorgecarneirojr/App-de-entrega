"use client";

import dynamic from "next/dynamic";
import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import { RouteInfo } from "@/lib/types";

const RouteMapCanvas = dynamic(() => import("@/components/route-map-canvas"), {
  ssr: false,
  loading: () => <div className="flex h-full items-center justify-center text-sm text-slate-500">Carregando mapa...</div>
});

type MapPoint = {
  latitude: number | null;
  longitude: number | null;
  label: string;
};

type DeliveryRouteMapProps = {
  origin: MapPoint;
  destination: MapPoint;
};

export function DeliveryRouteMap({ origin, destination }: DeliveryRouteMapProps) {
  const hasCoordinates =
    origin.latitude !== null &&
    origin.longitude !== null &&
    destination.latitude !== null &&
    destination.longitude !== null;

  const routeQuery = useQuery({
    queryKey: ["route", origin.latitude, origin.longitude, destination.latitude, destination.longitude],
    queryFn: async () => {
      const response = await api.get<RouteInfo>("/geo/route", {
        params: {
          from_lat: origin.latitude,
          from_lon: origin.longitude,
          to_lat: destination.latitude,
          to_lon: destination.longitude
        }
      });
      return response.data;
    },
    enabled: hasCoordinates,
    staleTime: 5 * 60 * 1000,
    retry: 1
  });

  if (!hasCoordinates) {
    return (
      <div role="status" className="rounded-2xl border border-dashed border-red-200 bg-white/70 p-4 text-sm text-slate-500">
        Selecione um endereco com localizacao confirmada para visualizar a rota.
      </div>
    );
  }

  const originPoint = {
    latitude: origin.latitude as number,
    longitude: origin.longitude as number,
    label: origin.label
  };
  const destinationPoint = {
    latitude: destination.latitude as number,
    longitude: destination.longitude as number,
    label: destination.label
  };

  const routeSummary = routeQuery.data
    ? `Rota de ${origin.label} para ${destination.label}: ${routeQuery.data.distance_km.toFixed(1)} quilometros, aproximadamente ${routeQuery.data.duration_min} minutos de carro.`
    : routeQuery.isError
      ? "Nao foi possivel calcular a rota agora."
      : "Calculando rota entre a loja e o endereco de entrega.";

  return (
    <div className="overflow-hidden rounded-2xl border border-red-100 bg-white">
      <div className="space-y-1 px-4 pt-3 text-sm">
        <p className="text-slate-600">
          <span className="font-semibold text-slate-900">De:</span> {origin.label}
        </p>
        <p className="text-slate-600">
          <span className="font-semibold text-slate-900">Para:</span> {destination.label}
        </p>
      </div>
      <p id="route-summary" className="sr-only" aria-live="polite">
        {routeSummary}
      </p>
      <div
        role="region"
        aria-label="Mapa interativo da rota de entrega"
        aria-describedby="route-summary"
        className="h-72 w-full"
      >
        <RouteMapCanvas
          origin={originPoint}
          destination={destinationPoint}
          geometry={routeQuery.data?.geometry ?? []}
        />
      </div>
      <div aria-live="polite" className="flex flex-wrap items-center justify-between gap-2 border-t border-red-100 px-4 py-3 text-sm">
        {routeQuery.isLoading && <span className="text-slate-500">Calculando rota...</span>}
        {routeQuery.isError && <span className="text-red-700">Nao foi possivel calcular a rota agora.</span>}
        {routeQuery.data && (
          <span className="font-semibold text-slate-800">
            {routeQuery.data.distance_km.toFixed(1)} km &bull; aproximadamente {routeQuery.data.duration_min} min de carro
          </span>
        )}
        <span className="text-xs uppercase tracking-wide text-slate-400">
          Rota: {routeQuery.data?.source === "estimado" ? "estimativa" : "OpenStreetMap/OSRM"}
        </span>
      </div>
    </div>
  );
}
