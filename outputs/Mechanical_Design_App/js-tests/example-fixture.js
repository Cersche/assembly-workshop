module.exports={
  "id": "eq-000000000004",
  "name": "Board example",
  "span": 1,
  "spec": {
    "name": "Board example",
    "dev_w": 85,
    "dev_d": 56,
    "dev_h": 20,
    "hole_d": 2.7,
    "standoff": 6,
    "insert_pilot": 3.2,
    "board_t": 1.6,
    "u": 1,
    "device_mount": "inserts",
    "joint": "screw",
    "rear_support": false,
    "dev_off_x": -1.5,
    "dev_off_y": 1,
    "dev_rot": 0,
    "holes": [
      [
        3.5,
        3.5
      ],
      [
        61.5,
        3.5
      ],
      [
        3.5,
        52.5
      ],
      [
        61.5,
        52.5
      ]
    ],
    "ports": [],
    "rear_ports": [],
    "keystones": [],
    "planning_ports": [
      {
        "id": "usb-c-power",
        "label": "USB-C power",
        "type": "usb-c",
        "x": -32.8,
        "y": 11.5,
        "z": 18.8,
        "points": "front",
        "face": null
      },
      {
        "id": "hdmi0",
        "label": "Micro-HDMI 0",
        "type": "micro-hdmi",
        "x": -18.05,
        "y": 11.2,
        "z": 18.8,
        "points": "front",
        "face": null
      },
      {
        "id": "hdmi1",
        "label": "Micro-HDMI 1",
        "type": "micro-hdmi",
        "x": -4.55,
        "y": 11.2,
        "z": 18.8,
        "points": "front",
        "face": null
      },
      {
        "id": "audio",
        "label": "Audio / composite 3.5 mm",
        "type": "other",
        "x": 10,
        "y": 10.6,
        "z": 20.6,
        "points": "front",
        "face": null
      },
      {
        "id": "usb2-lower",
        "label": "USB 2.0 (lower)",
        "type": "usb-a",
        "x": 45,
        "y": 22,
        "z": 21.4,
        "points": "right",
        "face": null
      },
      {
        "id": "usb2-upper",
        "label": "USB 2.0 (upper)",
        "type": "usb-a",
        "x": 45,
        "y": 22,
        "z": 29.4,
        "points": "right",
        "face": null
      },
      {
        "id": "usb3-lower",
        "label": "USB 3.0 (lower)",
        "type": "usb-a",
        "x": 44.6,
        "y": 40,
        "z": 21.4,
        "points": "right",
        "face": null
      },
      {
        "id": "usb3-upper",
        "label": "USB 3.0 (upper)",
        "type": "usb-a",
        "x": 44.6,
        "y": 40,
        "z": 29.4,
        "points": "right",
        "face": null
      },
      {
        "id": "ethernet",
        "label": "Ethernet",
        "type": "rj45",
        "x": 44.2,
        "y": 58.75,
        "z": 24.4,
        "points": "right",
        "face": null
      }
    ]
  },
  "status": "PROPOSED — UNVALIDATED",
  "parts": [],
  "example": true,
  "template": "equipment_tray.scad",
  "provenance": "Historical board dimensions and 58 × 49 mm hole pitch; connector centres from local reference mesh, ±2 mm. No reference mesh redistributed. Face, cable access, fit and strength UNKNOWN."
};
