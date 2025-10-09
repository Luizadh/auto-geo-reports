import React, { useState } from "react";
import "./DownloadButton.css";

const BASE_URL = "http://localhost:8001";


export function PdfDownloadButton({ inscricao, camposSelecionados, oficio, habilitado, observacao, destinatario }) {
  const [loading, setLoading] = useState(false);

  const handleDownload = async () => {
    try {
      setLoading(true);


     const response = await fetch(`${BASE_URL}/imovel/${inscricao}/pdf-com-observacao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
      camposSelecionados,
      oficio,
      observacao,
      destinatario
  })
});

      if (!response.ok) throw new Error("Erro ao gerar PDF");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      const nomeOficio = oficio.replace(/\//g, "-");
      a.href = url;
      a.download = `${nomeOficio}-${inscricao}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Não foi possível baixar o PDF");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleDownload}
      disabled={!habilitado || loading}
      className="download-button"
      style={{ marginTop: "10px", display: "flex", alignItems: "center", gap: "8px" }}
    >
      <div className="docs" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
        <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        {loading ? "Gerando documento..." : "Baixar PDF"}
      </div>

      <div className="download" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
        {loading ? (
          <div className="spinner"></div>
        ) : (
          <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
        )}
      </div>
    </button>
  );
}
