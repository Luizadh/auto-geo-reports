import React, { useState } from "react";

const onlyDigits12 = (s) => s.replace(/\D/g, "").slice(0, 12);


const formatInscricao = (digits) => {
  const s = onlyDigits12(digits);
  if (!s) return "";
  const a = s[0] || "";
  const b = s.slice(1, 4);
  const c = s.slice(4, 8);
  const d = s.slice(8, 11);
  const e = s.slice(11);

  let out = a;
  if (b) out += "." + b;
  if (c) out += "." + c;
  if (d) out += "." + d;
  if (e) out += "-" + e;
  return out;
};


export default function InscricaoInput({ value, onChange, ...props }) {
  const handleChange = (e) => {
    const digits = onlyDigits12(e.target.value);
    onChange?.(digits); 
  };

  
  return (
    <input
      type="text"
      inputMode="numeric"
      placeholder="0.000.0000.000-0"
      value={formatInscricao(value)}
      onChange={handleChange}
      {...props}
    />
  );
}
