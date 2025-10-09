const BASE_URL = "http://localhost:8001" 



export async function consultarImovel(inscricao, campos = [], numeroOficio = "") {
  
  
  const params = new URLSearchParams();
  campos.forEach(c => params.append("campos", c));

  if (numeroOficio) params.append("numeroOficio", numeroOficio);
  
  const url = `${BASE_URL}/imovel/${encodeURIComponent(inscricao)}${params.toString() ? `?${params.toString()}` : ""}`;
  const resp = await fetch(url);

  if (!resp.ok) {
    const txt = await resp.text().catch(() => null);
    throw new Error(txt || `Erro ${resp.status}`);
  }

  return await resp.json();
}

