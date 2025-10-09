import React from "react";

export function Checkbox({ label, checked, onChange, disabled }) {
  return (
    <label
      style={{
        display: "flex",
        alignItems: "center",
        gap: "8px",
        marginBottom: "8px",
      }}
    >
      <input
        type="checkbox"
        checked={checked}
        onChange={onChange}
        disabled={disabled} 
        style={{
          width: "16px",
          height: "16px",
          cursor: "pointer", 
        }}
      />
      {label && <span>{label}</span>} {}
    </label>
  );
}
