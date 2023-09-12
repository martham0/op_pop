const express = require('express');
const app = express ();
app.use(express.json());
const hostname = 'localhost';
const port = 3000

// info

class crew {
  constructor(name, age, position, luffyRank) {
    this.name = name;
    this.age = age;
    this.position = position;
    this.luffyRank = luffyRank;
  }
}

const sanji = new crew('Vinsmoke Sanji', 23, 'Cook','4');
const nami = new crew('Nami', 22, 'Navigator','2');
const zoro = new crew('Roronoa Zoro', 23, '2nd in command','1');
const luffy = new crew('Monkey D. Luffy', 21, 'Captain','0');
const usopp = new crew('Usopp', 19, 'Sniper','3');

const strawhat_crew = [sanji,nami,zoro,luffy,usopp]

app.listen(port,hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});


app.get("/status", (req,res) => {
  const status = {
    "Status": "Running"
 };
 res.send(status)
});

app.get("/strawhat-crew", (req,res) => {
  res.json(strawhat_crew)
  
})

// const http = require('http');
// const server = http.createServer((req, res) => {
//   res.statusCode = 200;
//   res.setHeader('Content-Type', 'text/plain');
//   res.end('Hello World');
// });
 