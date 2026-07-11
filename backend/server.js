
const express = require("express");
const cors = require("cors");
const app = express();
app.use(cors());
app.use(express.json());

app.post("/leaderboard", (req, res) => {
  console.log("Leaderboard update:", req.body);
  res.json({status: "success"});
});

app.post("/create-payment", (req, res) => {
  res.json({link: "https://checkout.flutterwave.com/payment?tx_ref=" + Date.now()});
});

app.listen(3000, () => console.log("Backend running on http://localhost:3000"));
