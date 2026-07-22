import React, { useState } from "react";

const VirtualTryOn = () => {
  const [personImage, setPersonImage] = useState(null);
  const [garmentImage, setGarmentImage] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!personImage || !garmentImage) {
      alert("Please upload both images!");
      return;
    }

    const formData = new FormData();
    formData.append("background", personImage);
    formData.append("garment", garmentImage);
    formData.append("garment_desc", "A stylish outfit");

    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/api/tryon/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setLoading(false);

      if (data.status === "✅ Success" && data.results) {
        setResults(data.results);
      } else {
        alert("Something went wrong! Check console.");
        console.error(data);
      }
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center p-8"
      style={{
        background: "linear-gradient(to right, #ffe0cc, #ffd6d6)",
      }}
    >
      <h1 className="text-4xl font-bold mb-8 flex items-center gap-2 text-gray-800">
        👗 Virtual Try-On
      </h1>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col sm:flex-row items-center gap-4 mb-8"
      >
        {/* Upload inputs */}
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setPersonImage(e.target.files[0])}
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setGarmentImage(e.target.files[0])}
        />

        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 rounded-lg text-white font-semibold"
          style={{
            background: "linear-gradient(to right, #ff7eb3, #ff758c)",
            opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? "Processing..." : "Try On"}
        </button>
      </form>

      {/* Output display */}
      {loading && (
        <p className="text-gray-600 mt-4">Generating your try-on... please wait.</p>
      )}

      {results.length > 0 && (
        <div className="flex flex-col sm:flex-row gap-6 mt-6 items-center justify-center">
          {results.map((res, i) => (
            <div key={i} className="flex flex-col items-center">
              <h3 className="font-semibold text-gray-700 mb-2 capitalize">
                {res.label.replace("_", " ")}
              </h3>
              <img
                src={res.url}
                alt={res.label}
                className="w-72 h-auto rounded-xl shadow-md border"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default VirtualTryOn;
