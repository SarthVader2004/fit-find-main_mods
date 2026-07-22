import React, { useState } from "react";
import "./BodyType.css";

const BodyType = () => {
  const [measurements, setMeasurements] = useState({
    bust: "",
    waist: "",
    hips: "",
    shoulders: "",
  });
  const [bodyType, setBodyType] = useState("");

  const handleChange = (e) => {
    setMeasurements({ ...measurements, [e.target.name]: e.target.value });
  };

  const calculateBodyType = () => {
    const { bust, waist, hips, shoulders } = measurements;
    if (!bust || !waist || !hips || !shoulders) {
      setBodyType("Please fill all measurements!");
      return;
    }

    const b = parseFloat(bust);
    const w = parseFloat(waist);
    const h = parseFloat(hips);
    const s = parseFloat(shoulders);

    let result = "";

    // 🧮 Simplified rules
    if (Math.abs(b - h) <= 5 && Math.abs(w - b) > 8) {
      result = "💃 Hourglass — Balanced bust and hips with defined waist.";
    } else if (h - b > 5 && h - s > 5) {
      result = "🍐 Pear — Hips wider than bust and shoulders.";
    } else if (b - h > 5 && s - h > 5) {
      result = "🔺 Inverted Triangle — Broad shoulders or bust, narrower hips.";
    } else if (Math.abs(b - h) <= 3 && Math.abs(h - s) <= 3 && Math.abs(w - b) <= 6) {
      result = "⬛ Rectangle — Similar measurements all around, minimal waist definition.";
    } else if (w >= b - 5 && w >= h - 5) {
      result = "🍎 Apple — Fuller midsection, less defined waist.";
    } else {
      result = "🕴 Oval — Slightly rounded body with gentle curves.";
    }

    setBodyType(result);
  };

  return (
    <div className="bodytype-container">
      <h2>👗 Body Shape Analyzer</h2>
      <p>Enter your measurements (in cm) to find your body type and style guidance.</p>

      <div className="input-group">
        <input
          type="number"
          name="bust"
          placeholder="Bust (cm)"
          value={measurements.bust}
          onChange={handleChange}
        />
        <input
          type="number"
          name="waist"
          placeholder="Waist (cm)"
          value={measurements.waist}
          onChange={handleChange}
        />
        <input
          type="number"
          name="hips"
          placeholder="Hips (cm)"
          value={measurements.hips}
          onChange={handleChange}
        />
        <input
          type="number"
          name="shoulders"
          placeholder="Shoulders (cm)"
          value={measurements.shoulders}
          onChange={handleChange}
        />
      </div>

      <button onClick={calculateBodyType}>Analyze</button>

      {bodyType && <p className="result">{bodyType}</p>}
    </div>
  );
};

export default BodyType;
