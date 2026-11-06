"use client";

import { useEffect } from "react";
import L from "leaflet";
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMap } from "react-leaflet";

type Point = {
  latitude: number;
  longitude: number;
  label: string;
};

type RouteMapCanvasProps = {
  origin: Point;
  destination: Point;
  geometry: [number, number][];
};

function markerIcon(letter: string, color: string) {
  return L.divIcon({
    className: "",
    html: `<span style="display:flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:9999px;background:${color};color:#fff;font-weight:700;font-size:13px;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.35)">${letter}</span>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -16]
  });
}

function FitBounds({ positions }: { positions: [number, number][] }) {
  const map = useMap();

  useEffect(() => {
    if (positions.length) {
      map.fitBounds(L.latLngBounds(positions).pad(0.2));
    }
  }, [map, positions]);

  return null;
}

export default function RouteMapCanvas({ origin, destination, geometry }: RouteMapCanvasProps) {
  const storeIcon = markerIcon("L", "#b91c1c");
  const addressIcon = markerIcon("E", "#1d4ed8");
  const positions = geometry.length
    ? geometry
    : [
        [origin.latitude, origin.longitude] as [number, number],
        [destination.latitude, destination.longitude] as [number, number]
      ];

  return (
    <MapContainer
      center={[origin.latitude, origin.longitude]}
      zoom={14}
      scrollWheelZoom={false}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[origin.latitude, origin.longitude]} icon={storeIcon}>
        <Popup>{origin.label}</Popup>
      </Marker>
      <Marker position={[destination.latitude, destination.longitude]} icon={addressIcon}>
        <Popup>{destination.label}</Popup>
      </Marker>
      <Polyline positions={positions} pathOptions={{ color: "#b91c1c", weight: 5, opacity: 0.8 }} />
      <FitBounds positions={positions} />
    </MapContainer>
  );
}
