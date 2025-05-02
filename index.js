const mqtt = require("mqtt");
const fs = require("fs");

// REPLACE THE FOLLOWING WITH YOUR OWN VALUES
const BROKER = "a325o3szmlqb5j-ats.iot.us-east-2.amazonaws.com"// should look similar to: example-ats.iot.us-east-1å.amazonaws.com;
const THING_NAME = "IoTDevice1"
const CERT_FILE_NAME = "Device.crt"
const PRIVATE_KEY_FILE_NAME = "private.key"


const options = {
  rejectUnauthorized: false,
  port: 8883,
  host: BROKER,
  clientId: THING_NAME,
  cert: fs.readFileSync(`./${CERT_FILE_NAME}`, "utf8"),
  key: fs.readFileSync(`./${PRIVATE_KEY_FILE_NAME}`, "utf8"),
  connectTimeout: 10_000,
};
const client = mqtt.connect(`mqtts://${BROKER}`, options);

client.on("connect", () => {
  console.log("connected");
  setInterval(function() {
    console.log(new Date().getSeconds())
    client.publish(THING_NAME, JSON.stringify([
    {
      "label": "Accelerometer",
      "display_type": "line_graph",
      "unit": "meters",
      "values": [
        {
          "value": Math.floor(Math.random() * 101),
          "label": "x"
        },
        {
          "value": Math.floor(Math.random() * 101),
          "label": "y"
        },
        {
          "value": Math.floor(Math.random() * 101),
          "label": "z"
        }
      ]
    },
    {
      "label": "Gyroscope",
      "display_type": "line_graph",
      "unit": "meters",
      "values": [
        {
          "value": Math.floor(Math.random() * 101),
          "label": "x"
        },
        {
          "value": Math.floor(Math.random() * 101),
          "label": "y"
        },
        {
          "value": Math.floor(Math.random() * 101),
          "label": "z"
        }
      ]
    },
    {
      "label": "Battery",
      "display_type": "donut_graph",
      "unit": "%",
      "values": [
        {
          "value": 72,
          "label": "Charged"
        }
      ]
    },
    {
      "label": "GPS",
      "display_type": "map",
      "unit": "",
      "values": [
        {
          "value": -122.33328,
          "label": "Longitude"
        },
        {
          "value": 47.61544,
          "label": "Latitude"
        },
        {
          "value": 118732,
          "label": "Accuracy (m)"
        }
      ]
    }
  ]));
}, 15000);
});

client.on("reconnect", () => {
  console.warn('reconnecting')
})
