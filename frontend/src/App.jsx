import { useState, useEffect } from "react";
import axios from "axios";

function App() {
const [file, setFile] = useState(null);
const [preview, setPreview] = useState(null);
const [result, setResult] = useState(null);
const [loading, setLoading] = useState(false);

const [form, setForm] = useState({
N: "", P: "", K: "", pH: "",
EC: "", OC: "", S: "",
Zn: "", Fe: "", Cu: "",
Mn: "", B: ""
});

const [errors, setErrors] = useState({});

const ranges = {
N: [0, 500], P: [0, 100], K: [0, 800], pH: [0, 14],
EC: [0, 10], OC: [0, 5], S: [0, 50],
Zn: [0, 5], Fe: [0, 10], Cu: [0, 5],
Mn: [0, 10], B: [0, 5]
};

useEffect(() => {
validate();
}, [form, file]);

const handleFile = (e) => {
const f = e.target.files[0];
setFile(f);
if (f) setPreview(URL.createObjectURL(f));
};

const handleChange = (e) => {
setForm({ ...form, [e.target.name]: e.target.value });
};

const validate = () => {
let newErrors = {};


Object.keys(form).forEach((key) => {
  const value = parseFloat(form[key]);

  if (!form[key]) {
    newErrors[key] = "Required";
  } else if (value < ranges[key][0] || value > ranges[key][1]) {
    newErrors[key] = `Range ${ranges[key][0]} - ${ranges[key][1]}`;
  }
});

if (!file) newErrors.file = "Upload image";

setErrors(newErrors);
return Object.keys(newErrors).length === 0;


};

const handlePredict = async () => {
if (!validate()) return;


const formData = new FormData();
formData.append("file", file);

const npkString = Object.values(form).join(",");
formData.append("npk", npkString);

try {
  setLoading(true);

  const res = await axios.post(
    "http://localhost:8090/api/predict",
    formData
  );

  const soil = res.data?.soil_type
    ? res.data.soil_type.replaceAll("_", " ")
    : "Unknown Soil";

  setResult({
    ...res.data,
    soil_type: soil
  });

} catch (err) {
  console.error(err);
} finally {
  setLoading(false);
}


};

return ( <div className="flex h-screen bg-gradient-to-br from-blue-900 via-indigo-900 to-black text-white">


  {/* SIDEBAR */}
  <div className="w-64 bg-white/10 backdrop-blur-lg p-6 flex flex-col">
    <h2 className="text-2xl font-bold mb-6">🌱 Soil AI</h2>

    <nav className="space-y-3">
      <div className="hover:bg-white/20 p-2 rounded">Dashboard</div>
      <div className="hover:bg-white/20 p-2 rounded">Prediction</div>
      <div className="hover:bg-white/20 p-2 rounded">Analytics</div>
    </nav>
  </div>

  {/* MAIN */}
  <div className="flex-1 p-6 overflow-auto">

    <h1 className="text-3xl font-bold mb-6">
      Soil AI Dashboard
    </h1>

    {/* GLASS CARD */}
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 shadow-lg">

      {/* IMAGE */}
      <div className="flex gap-6 mb-6">
        <div className="w-40 h-40 bg-white/20 rounded-xl flex items-center justify-center overflow-hidden">
          {preview ? (
            <img src={preview} className="w-full h-full object-cover"/>
          ) : "Preview"}
        </div>

        <div>
          <input type="file" onChange={handleFile} />
          {errors.file && (
            <p className="text-red-400 text-sm">{errors.file}</p>
          )}
        </div>
      </div>

      {/* INPUTS */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        {Object.keys(form).map((key) => (
          <div key={key}>
            <input
              name={key}
              placeholder={`${key} (${ranges[key][0]}-${ranges[key][1]})`}
              value={form[key]}
              onChange={handleChange}
              className="bg-white/20 p-2 rounded text-white placeholder-gray-300 w-full"
            />
            {errors[key] && (
              <p className="text-red-400 text-xs">
                {errors[key]}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* BUTTON */}
      <button
        onClick={handlePredict}
        className="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded-xl"
      >
        {loading ? "Analyzing..." : "Predict"}
      </button>

      {/* RESULT */}
      {result && (
        <div className="mt-6 text-center bg-white/10 p-4 rounded-xl">
          <h2 className="text-xl font-bold">Result</h2>
          <p>Soil: {result.soil_type}</p>
          <p>Fertility: {result.fertility}</p>
        </div>
      )}

    </div>
  </div>
</div>


);
}

export default App;
