import React from "react";

export function Card({ title, children }) {
  return (
  <div
      style={{
        backgroundColor: "#fff",                
        color: "#000",                          
        display: "flex",                    
        flexDirection: "column",               
        gap: "1.5rem",                        
        borderRadius: "0.75rem",                
        border: "1px solid #ccc",              
        paddingTop: "1.5rem",                   
        paddingBottom: "1.5rem",                
        boxShadow: "0 1px 2px rgba(133, 132, 132, 0.05)",
        maxWidth: "500px",
        margin: "1rem auto",
        padding:"20px"
      }}
    >
      {title && <h3 style={{ marginBottom: "0.5rem" }}>{title}</h3>}
      <div>{children}</div>
    </div>
  );
}