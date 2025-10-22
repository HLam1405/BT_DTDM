const express = require("express");
const sql = require("mssql");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // phục vụ file index.html

// ⚙️ Cấu hình SQL Azure (thay giá trị thật của bạn)
const dbConfig = {
  user: "hoanglam",
  password: "Something123@",
  server: 'hienthi.database.windows.net', // kiểm tra lại tên server trong SSMS
  database: "HienThiDB",
  options: {
    encrypt: true,
    trustServerCertificate: false
  },
};

// ✅ Route chính: nếu không tìm thấy file -> trả về index.html
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ➕ API thêm dữ liệu
app.post("/api/add", async (req, res) => {
  try {
    const { message } = req.body;
    if (!message) return res.status(400).json({ error: "Thiếu message" });

    const pool = await sql.connect(dbConfig);
    await pool.request().input("msg", sql.NVarChar(100), message)
      .query("INSERT INTO Greetings (message) VALUES (@msg)");
    res.json({ success: true });
  } catch (err) {
    console.error("Lỗi thêm:", err);
    res.status(500).json({ error: "Lỗi thêm dữ liệu" });
  }
});

// 🎲 API lấy ngẫu nhiên
app.get("/api/random", async (req, res) => {
  try {
    const pool = await sql.connect(dbConfig);
    const result = await pool.request().query("SELECT TOP 1 * FROM Greetings ORDER BY NEWID()");
    if (result.recordset.length === 0) return res.status(404).json({ error: "Chưa có dữ liệu" });
    res.json(result.recordset[0]);
  } catch (err) {
    console.error("Lỗi lấy:", err);
    res.status(500).json({ error: "Lỗi lấy dữ liệu" });
  }
});

// ❌ API xóa tất cả
app.delete("/api/clear", async (req, res) => {
  try {
    const pool = await sql.connect(dbConfig);
    await pool.request().query("DELETE FROM Greetings");
    res.json({ success: true });
  } catch (err) {
    console.error("Lỗi xóa:", err);
    res.status(500).json({ error: "Lỗi xóa dữ liệu" });
  }
});

// 🚀 Khởi động
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server đang chạy tại http://localhost:${PORT}`));


//const dbConfig = {
  //user: "hoanglam",
  //password: "Something123@",
  //server: 'hienthi.database.windows.net', // kiểm tra lại tên server trong SSMS
  //database: "HienThiDB",
  //options: {
    //encrypt: true,
    //trustServerCertificate: false
  //},
//};
