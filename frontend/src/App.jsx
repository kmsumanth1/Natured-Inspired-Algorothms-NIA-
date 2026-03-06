import { useState, useEffect } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    N: "", P: "", K: "", pH: "",
    EC: "", OC: "", S: "",
    Zn: "", Fe: "", Cu: "",
    Mn: "", B: ""
  });

  const [errors, setErrors] = useState({});

  // Realistic soil color mapping
const SOIL_COLORS = {
  Black_Soil: "#2E2E2E",        // Dark Black
  Red_Soil: "#C0392B",          // Natural Red
  Laterite_Soil: "#8B4513",     // Reddish Brown
  Alluvial_Soil: "#D2B48C",     // Light Brown / Sandy
  Clay_Soil: "#A0522D",         // Brown Clay
  Sandy_Soil: "#EDC9AF",        // Sand Color
  Loamy_Soil: "#6B8E23"         // Olive Brown (Fertile)
};

  const ranges = {
    N: [0, 500],
    P: [0, 100],
    K: [0, 800],
    pH: [0, 14],
    EC: [0, 10],
    OC: [0, 5],
    S: [0, 50],
    Zn: [0, 5],
    Fe: [0, 10],
    Cu: [0, 5],
    Mn: [0, 10],
    B: [0, 5]
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
        newErrors[key] = `Must be ${ranges[key][0]} - ${ranges[key][1]}`;
      }
    });

    if (!file) newErrors.file = "Image required";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handlePredict = async () => {
    if (!validate()) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("npk", Object.values(form).join(","));

    try {
      setLoading(true);
      const response = await axios.post(
  "https://soil-ai-backend.onrender.com/predict",
  formData
);
      setResult(response.data);
      fetchHistory();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    const response = await axios.get("http://localhost:8080/api/history");
    setHistory(response.data);
  };

  const toggleHistory = async () => {
    if (!showHistory) await fetchHistory();
    setShowHistory(!showHistory);
  };

  const getBadgeColor = (fertility) => {
    if (fertility === "High") return "bg-green-600";
    if (fertility === "Medium") return "bg-yellow-500";
    return "bg-red-600";
  };

  const soilChartData = Object.values(
    history.reduce((acc, item) => {
      acc[item.soilType] = acc[item.soilType] || {
        name: item.soilType,
        value: 0
      };
      acc[item.soilType].value += 1;
      return acc;
    }, {})
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-200 via-green-300 to-green-500 p-8">
      <div className="max-w-6xl mx-auto">

        <h1 className="text-3xl font-bold text-center mb-8">
          🌱 Soil AI Premium Dashboard
        </h1>

        {/* Prediction Card */}
        <div className="bg-white shadow-xl rounded-2xl p-6 mb-8">

          <input
            type="file"
            className="w-full mb-2 border p-2 rounded-lg"
            onChange={(e) => setFile(e.target.files[0])}
          />
          {errors.file && (
            <p className="text-red-500 text-sm mb-2">
              {errors.file}
            </p>
          )}

          <div className="grid grid-cols-3 gap-4 mb-4">
            {Object.keys(form).map((field) => (
              <div key={field}>
                <input
                  type="number"
                  name={field}
                  placeholder={`${field} (${ranges[field][0]}-${ranges[field][1]})`}
                  value={form[field]}
                  onChange={handleChange}
                  min={ranges[field][0]}
                  max={ranges[field][1]}
                  className="w-full border p-2 rounded-lg"
                />
                {errors[field] && (
                  <p className="text-red-500 text-sm mt-1">
                    {errors[field]}
                  </p>
                )}
              </div>
            ))}
          </div>

          <button
            onClick={handlePredict}
            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          >
            {loading ? "Predicting..." : "Predict"}
          </button>

          {result && (
            <div className="mt-6 text-center">
              <p className="text-lg font-semibold">
                Soil Type: {result.soil_type}
              </p>

              <span
                className={`inline-block mt-2 px-4 py-1 rounded-full text-white font-semibold ${getBadgeColor(
                  result.fertility
                )}`}
              >
                {result.fertility}
              </span>
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white shadow-lg rounded-xl p-4 text-center">
            <h2 className="text-xl font-bold">{history.length}</h2>
            <p>Total Predictions</p>
          </div>
          <div className="bg-white shadow-lg rounded-xl p-4 text-center">
            <h2 className="text-xl font-bold">
              {history.filter(h => h.fertility === "High").length}
            </h2>
            <p>High Fertility</p>
          </div>
          <div className="bg-white shadow-lg rounded-xl p-4 text-center">
            <h2 className="text-xl font-bold">
              {history.filter(h => h.fertility === "Low").length}
            </h2>
            <p>Low Fertility</p>
          </div>
        </div>

        {/* Chart */}
        <div className="bg-white shadow-xl rounded-2xl p-6 mb-8">
          <h2 className="text-xl font-bold mb-4 text-center">
            Soil Distribution
          </h2>

          <ResponsiveContainer width="100%" height={320}>
  <PieChart>
    <Pie
      data={soilChartData}
      dataKey="value"
      nameKey="name"
      cx="50%"
      cy="50%"
      innerRadius={60}        // Makes it a donut chart
      outerRadius={120}
      paddingAngle={4}        // Small spacing between slices
      label={({ name, percent }) =>
        `${name} ${(percent * 100).toFixed(0)}%`
      }
      isAnimationActive={true}
    >
      {soilChartData.map((entry, index) => (
        <Cell
          key={`cell-${index}`}
          fill={SOIL_COLORS[entry.name] || "#8884d8"}
        />
      ))}
    </Pie>

    <Tooltip
      formatter={(value) => [`${value} Predictions`, "Count"]}
    />

    <Legend
      verticalAlign="bottom"
      height={36}
    />
  </PieChart>
</ResponsiveContainer>
        </div>

        {/* History Toggle */}
        <button
          onClick={toggleHistory}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition mb-4"
        >
          {showHistory ? "Hide History" : "View History"}
        </button>

        <div
          className={`overflow-hidden transition-all duration-500 ${
            showHistory ? "max-h-[1000px]" : "max-h-0"
          }`}
        >
          {history.length > 0 && (
            <table className="w-full bg-white shadow-lg rounded-xl">
              <thead>
                <tr className="bg-gray-200">
                  <th className="p-2">ID</th>
                  <th className="p-2">Soil Type</th>
                  <th className="p-2">Fertility</th>
                  <th className="p-2">NPK</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id} className="text-center border-t">
                    <td className="p-2">{item.id}</td>
                    <td className="p-2">{item.soilType}</td>
                    <td className="p-2">
                      <span
                        className={`px-3 py-1 rounded-full text-white text-sm ${getBadgeColor(
                          item.fertility
                        )}`}
                      >
                        {item.fertility}
                      </span>
                    </td>
                    <td className="p-2">{item.npkValues}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;