import React, { useState } from "react";
import RelatorioForm from "./forms/RelatorioForm";
import { Card } from "./components/Card";

function App() {
  const [checked, setChecked] = useState(false);

  return (
    <div className="p-4">
      <h1 style={styles.h1}>Gerador de Relatório de Lote</h1>

      <Card className="card-full-height">
        <RelatorioForm />
      </Card>

  
    </div>
  );
}
export default App;


const styles = {

  h1: {
    marginTop: '70px',
    fontSize: '30px',
    fontWeight: 'bold',
    marginBottom: '70px',
  },
}




