import React, { useState } from "react";
import { Checkbox }  from "../components/Checkbox";
import "./RelatorioForm.css";
import { consultarImovel } from "../services/api";
import { PdfDownloadButton } from "../components/DownloadButton";
import InscricaoInput from "../components/InscricaoInput";
import Select from 'react-select'
import DestinatarioSelect from "../components/DestinatarioSelect";


function RelatorioForm() {
  const [inscricao, setInscricao] = useState("");
  const [oficio, setOficio] = useState("");
  const [selecionados, setSelecionados] = useState(["INSCRICAO"]);
  const [mensagem, setMensagem] = useState("");
  const [destinatario, setDestinatario] = useState("");
  const [erro, setErro] = useState("");
  const [observacao, setObservacao] = useState("");
  const [loading, setLoading] = useState(false);
  
  const opcoesCampos = [
    { key: "INSCRICAO", label: "Inscrição" },
    { key: "PROPRIETARIO", label: "Proprietário" },
    { key: "CPFCGC", label: "CPF/CGC" },
    { key: "LOCALIZIMOVEL", label: "Logradouro" },
    { key: "NUMERO", label: "Número" },
    { key: "BAIRRO", label: "Bairro" },
    { key: "LOTEAMENTO", label: "Loteamento" },
    { key: "AREADOLOTE", label: "Área do Lote" },
    { key: "AREACONSTRUIDA", label: "Área Construída" },
    { key: "TIPOIMOVEL", label: "Tipo do Imóvel" },
  ];


  const handleCheckboxChange = (key) => {
     if (key === "INSCRICAO") return; 

  if (selecionados.includes(key)) {
    setSelecionados(selecionados.filter((c) => c !== key));
  } else {
    setSelecionados([...selecionados, key]);
  }
};
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setMensagem("");
    setLoading(true);
    console.log("Vai pro backend:", inscricao); 

    
    try {
  
      const dados = await consultarImovel(inscricao, selecionados, oficio);

      setMensagem(JSON.stringify(dados, null, 2));

  
    } catch (err) {  try {
    const data = await err.response?.json();
    setErro(data?.detail || "INSCRIÇÃO MUNICIPAL NÃO ENCONTRADA");
  } catch {
    setErro("Erro ao buscar dados do imóvel!");
  }
    } finally {
      setLoading(false);
    }
  };


  return (
      <div className="form-container-wrapper">
      <form onSubmit={handleSubmit} className="form-container">
        <label>Inscrição Municipal:</label>
        <InscricaoInput
          type="text"
          placeholder="0.000.0000.000-0"
          value={inscricao}
          onChange={setInscricao}
          className="input"
          required
        />
        
        <button type="submit" className="button" disabled={loading}>
          {loading ? "Buscando..." : "Consultar"}
        </button>
        {loading && <p>Carregando...</p>}
      {erro && <p className="erro">{erro}</p>}
      
  {mensagem && (
    
    <>
    <h3>Lote Encontrado!</h3>
        <label>Destinatário:*</label>
        <DestinatarioSelect
        value={destinatario}
        onChange={setDestinatario}
        options={[
    "Defensoria Pública do Estado do Rio de Janeiro",
    "Ministério Publico do Rio de Janeiro",
    ]}
    isDisabled={!mensagem}
    
    
        />
        
        <label>Documento:*</label>
        <input 
        type="text"
        value={oficio}
        onChange={(e) => setOficio(e.target.value)}
        className="input"
        placeholder="Ex: Ofício V11/2024"
        disabled={!mensagem}
        
        
        />

        <label>Observação: </label>
        <textarea
        placeholder="(opicional)"
        value={observacao}
        onChange={(e) => setObservacao(e.target.value)}
        disabled={!mensagem}
      
      />

        <label style={{ fontWeight: "bold", marginTop: "10px", fontSize: "20px" }}>
          Incluir no relatório:
        </label>
        <div>
      
       <Checkbox
          key="SELECT_ALL"
          label="Selecionar todos"
          checked={selecionados.length === opcoesCampos.length}
          disabled={!mensagem} 
          onChange={() => {
          if (selecionados.length === opcoesCampos.length) {
              setSelecionados(["INSCRICAO"]); 
          } else {
              setSelecionados(opcoesCampos.map(opt => opt.key)); 
          if (!selecionados.includes("INSCRICAO")) {
              setSelecionados(prev => [...new Set([...prev, "INSCRICAO"])]);
          }
          }
          }}
/>
          {opcoesCampos.map((opt) => (
            <Checkbox
              key={opt.key}
              label={opt.label}
              checked={selecionados.includes(opt.key)}
              onChange={() => handleCheckboxChange(opt.key)}
              disabled={opt.key === "INSCRICAO" || !mensagem} 
            />
          ))}
        </div>
  </>
        )}

      </form>

     
      {mensagem && (
        <div className="footer">
   
          <PdfDownloadButton 
      inscricao={inscricao}
      camposSelecionados={selecionados}
      oficio={oficio}
      habilitado={!!mensagem && destinatario && oficio}
      destinatario={destinatario}
      observacao={observacao}
    />

        </div>
      )}
    </div>
  );
}

export default RelatorioForm;



