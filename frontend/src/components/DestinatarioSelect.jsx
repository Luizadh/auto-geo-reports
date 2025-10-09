import React from "react";
import CreatableSelect from "react-select/creatable";

function DestinatarioSelect({ value, onChange, options, isDisabled }) {

    const customStyles = {
  dropdownIndicator: (provided) => ({
    ...provided,
    display: "none"  
  }),
};

  const selectOptions = options.map((opt) => ({ value: opt, label: opt }));


  const handleChange = (selectedOption) => {
    if (selectedOption) {
      onChange(selectedOption.value);
    } else {
      onChange("");
    }
  };

  return (
    <CreatableSelect
      value={value ? { value, label: value } : null}
      onChange={handleChange}
      options={selectOptions}
      isClearable
      isDisabled={isDisabled}
       styles={customStyles}
      placeholder="Digite..."
    />
  );
}

export default DestinatarioSelect;
