# -*- coding: utf-8 -*-
from typing import Dict, List, Union

LOG_FOLDER = "log"
LOG_FILE = LOG_FOLDER + "/error.log"
CMD_CHANNEL_NAME = "CMD_ASWDB"
CONFIG_FILE_NAME = "settings.ini"
SECTION_NAME = "Settings"
KEY_WATCH_WORLD = "WATCH_WORLD"
KEY_WATCH_INTERVAL = "WATCH_INTERVAL"
KEY_PLAYER_SBN_COUNT = "SEND_MESSAGE_PLAYER_COUNT_SBN"
KEY_BLACKLIST = "BLACK_LIST_PLAYER"
KEY_TOKEN = "BOT_TOKEN"
URL_CLUSTER_SERVER = "https://atlas.hgn.hu/api/cluster/{}/servers"
URL_SERVER_PLAYER = "https://atlas.hgn.hu/api/server/{}/players"

CLUSTERS: List[Dict[str, Union[int, str]]] = [
    {"id": 1, "name": "NA - PvE"},
    {"id": 2, "name": "NA - PvP"},
    {"id": 3, "name": "EU - PvE"},
    {"id": 4, "name": "EU - PvP"},
]

SERVER_NAMES = [{'id': 1, 'name': 'A1'}, {'id': 2, 'name': 'A2'}, {'id': 3, 'name': 'A3'}, {'id': 4, 'name': 'A4'},
                {'id': 5, 'name': 'A5'}, {'id': 6, 'name': 'A6'}, {'id': 7, 'name': 'A7'}, {'id': 8, 'name': 'A8'},
                {'id': 9, 'name': 'A9'}, {'id': 10, 'name': 'A10'}, {'id': 11, 'name': 'A11'},
                {'id': 12, 'name': 'A12'}, {'id': 13, 'name': 'A13'}, {'id': 14, 'name': 'A14'},
                {'id': 15, 'name': 'A15'}, {'id': 16, 'name': 'B1'}, {'id': 17, 'name': 'B2'},
                {'id': 18, 'name': 'B3'}, {'id': 19, 'name': 'B4'}, {'id': 20, 'name': 'B5'},
                {'id': 21, 'name': 'B6'}, {'id': 22, 'name': 'B7'}, {'id': 23, 'name': 'B8'},
                {'id': 24, 'name': 'B9'}, {'id': 25, 'name': 'B10'}, {'id': 26, 'name': 'B11'},
                {'id': 27, 'name': 'B12'}, {'id': 28, 'name': 'B13'}, {'id': 29, 'name': 'B14'},
                {'id': 30, 'name': 'B15'}, {'id': 31, 'name': 'C1'}, {'id': 32, 'name': 'C2'},
                {'id': 33, 'name': 'C3'}, {'id': 34, 'name': 'C4'}, {'id': 35, 'name': 'C5'},
                {'id': 36, 'name': 'C6'}, {'id': 37, 'name': 'C7'}, {'id': 38, 'name': 'C8'},
                {'id': 39, 'name': 'C9'}, {'id': 40, 'name': 'C10'}, {'id': 41, 'name': 'C11'},
                {'id': 42, 'name': 'C12'}, {'id': 43, 'name': 'C13'}, {'id': 44, 'name': 'C14'},
                {'id': 45, 'name': 'C15'}, {'id': 46, 'name': 'D1'}, {'id': 47, 'name': 'D2'},
                {'id': 48, 'name': 'D3'}, {'id': 49, 'name': 'D4'}, {'id': 50, 'name': 'D5'},
                {'id': 51, 'name': 'D6'}, {'id': 52, 'name': 'D7'}, {'id': 53, 'name': 'D8'},
                {'id': 54, 'name': 'D9'}, {'id': 55, 'name': 'D10'}, {'id': 56, 'name': 'D11'},
                {'id': 57, 'name': 'D12'}, {'id': 58, 'name': 'D13'}, {'id': 59, 'name': 'D14'},
                {'id': 60, 'name': 'D15'}, {'id': 61, 'name': 'E1'}, {'id': 62, 'name': 'E2'},
                {'id': 63, 'name': 'E3'}, {'id': 64, 'name': 'E4'}, {'id': 65, 'name': 'E5'},
                {'id': 66, 'name': 'E6'}, {'id': 67, 'name': 'E7'}, {'id': 68, 'name': 'E8'},
                {'id': 69, 'name': 'E9'}, {'id': 70, 'name': 'E10'}, {'id': 71, 'name': 'E11'},
                {'id': 72, 'name': 'E12'}, {'id': 73, 'name': 'E13'}, {'id': 74, 'name': 'E14'},
                {'id': 75, 'name': 'E15'}, {'id': 76, 'name': 'F1'}, {'id': 77, 'name': 'F2'},
                {'id': 78, 'name': 'F3'}, {'id': 79, 'name': 'F4'}, {'id': 80, 'name': 'F5'},
                {'id': 81, 'name': 'F6'}, {'id': 82, 'name': 'F7'}, {'id': 83, 'name': 'F8'},
                {'id': 84, 'name': 'F9'}, {'id': 85, 'name': 'F10'}, {'id': 86, 'name': 'F11'},
                {'id': 87, 'name': 'F12'}, {'id': 88, 'name': 'F13'}, {'id': 89, 'name': 'F14'},
                {'id': 90, 'name': 'F15'}, {'id': 91, 'name': 'G1'}, {'id': 92, 'name': 'G2'},
                {'id': 93, 'name': 'G3'}, {'id': 94, 'name': 'G4'}, {'id': 95, 'name': 'G5'},
                {'id': 96, 'name': 'G6'}, {'id': 97, 'name': 'G7'}, {'id': 98, 'name': 'G8'},
                {'id': 99, 'name': 'G9'}, {'id': 100, 'name': 'G10'}, {'id': 101, 'name': 'G11'},
                {'id': 102, 'name': 'G12'}, {'id': 103, 'name': 'G13'}, {'id': 104, 'name': 'G14'},
                {'id': 105, 'name': 'G15'}, {'id': 106, 'name': 'H1'}, {'id': 107, 'name': 'H2'},
                {'id': 108, 'name': 'H3'}, {'id': 109, 'name': 'H4'}, {'id': 110, 'name': 'H5'},
                {'id': 111, 'name': 'H6'}, {'id': 112, 'name': 'H7'}, {'id': 113, 'name': 'H8'},
                {'id': 114, 'name': 'H9'}, {'id': 115, 'name': 'H10'}, {'id': 116, 'name': 'H11'},
                {'id': 117, 'name': 'H12'}, {'id': 118, 'name': 'H13'}, {'id': 119, 'name': 'H14'},
                {'id': 120, 'name': 'H15'}, {'id': 121, 'name': 'I1'}, {'id': 122, 'name': 'I2'},
                {'id': 123, 'name': 'I3'}, {'id': 124, 'name': 'I4'}, {'id': 125, 'name': 'I5'},
                {'id': 126, 'name': 'I6'}, {'id': 127, 'name': 'I7'}, {'id': 128, 'name': 'I8'},
                {'id': 129, 'name': 'I9'}, {'id': 130, 'name': 'I10'}, {'id': 131, 'name': 'I11'},
                {'id': 132, 'name': 'I12'}, {'id': 133, 'name': 'I13'}, {'id': 134, 'name': 'I14'},
                {'id': 135, 'name': 'I15'}, {'id': 136, 'name': 'J1'}, {'id': 137, 'name': 'J2'},
                {'id': 138, 'name': 'J3'}, {'id': 139, 'name': 'J4'}, {'id': 140, 'name': 'J5'},
                {'id': 141, 'name': 'J6'}, {'id': 142, 'name': 'J7'}, {'id': 143, 'name': 'J8'},
                {'id': 144, 'name': 'J9'}, {'id': 145, 'name': 'J10'}, {'id': 146, 'name': 'J11'},
                {'id': 147, 'name': 'J12'}, {'id': 148, 'name': 'J13'}, {'id': 149, 'name': 'J14'},
                {'id': 150, 'name': 'J15'}, {'id': 151, 'name': 'K1'}, {'id': 152, 'name': 'K2'},
                {'id': 153, 'name': 'K3'}, {'id': 154, 'name': 'K4'}, {'id': 155, 'name': 'K5'},
                {'id': 156, 'name': 'K6'}, {'id': 157, 'name': 'K7'}, {'id': 158, 'name': 'K8'},
                {'id': 159, 'name': 'K9'}, {'id': 160, 'name': 'K10'}, {'id': 161, 'name': 'K11'},
                {'id': 162, 'name': 'K12'}, {'id': 163, 'name': 'K13'}, {'id': 164, 'name': 'K14'},
                {'id': 165, 'name': 'K15'}, {'id': 166, 'name': 'L1'}, {'id': 167, 'name': 'L2'},
                {'id': 168, 'name': 'L3'}, {'id': 169, 'name': 'L4'}, {'id': 170, 'name': 'L5'},
                {'id': 171, 'name': 'L6'}, {'id': 172, 'name': 'L7'}, {'id': 173, 'name': 'L8'},
                {'id': 174, 'name': 'L9'}, {'id': 175, 'name': 'L10'}, {'id': 176, 'name': 'L11'},
                {'id': 177, 'name': 'L12'}, {'id': 178, 'name': 'L13'}, {'id': 179, 'name': 'L14'},
                {'id': 180, 'name': 'L15'}, {'id': 181, 'name': 'M1'}, {'id': 182, 'name': 'M2'},
                {'id': 183, 'name': 'M3'}, {'id': 184, 'name': 'M4'}, {'id': 185, 'name': 'M5'},
                {'id': 186, 'name': 'M6'}, {'id': 187, 'name': 'M7'}, {'id': 188, 'name': 'M8'},
                {'id': 189, 'name': 'M9'}, {'id': 190, 'name': 'M10'}, {'id': 191, 'name': 'M11'},
                {'id': 192, 'name': 'M12'}, {'id': 193, 'name': 'M13'}, {'id': 194, 'name': 'M14'},
                {'id': 195, 'name': 'M15'}, {'id': 196, 'name': 'N1'}, {'id': 197, 'name': 'N2'},
                {'id': 198, 'name': 'N3'}, {'id': 199, 'name': 'N4'}, {'id': 200, 'name': 'N5'},
                {'id': 201, 'name': 'N6'}, {'id': 202, 'name': 'N7'}, {'id': 203, 'name': 'N8'},
                {'id': 204, 'name': 'N9'}, {'id': 205, 'name': 'N10'}, {'id': 206, 'name': 'N11'},
                {'id': 207, 'name': 'N12'}, {'id': 208, 'name': 'N13'}, {'id': 209, 'name': 'N14'},
                {'id': 210, 'name': 'N15'}, {'id': 211, 'name': 'O1'}, {'id': 212, 'name': 'O2'},
                {'id': 213, 'name': 'O3'}, {'id': 214, 'name': 'O4'}, {'id': 215, 'name': 'O5'},
                {'id': 216, 'name': 'O6'}, {'id': 217, 'name': 'O7'}, {'id': 218, 'name': 'O8'},
                {'id': 219, 'name': 'O9'}, {'id': 220, 'name': 'O10'}, {'id': 221, 'name': 'O11'},
                {'id': 222, 'name': 'O12'}, {'id': 223, 'name': 'O13'}, {'id': 224, 'name': 'O14'},
                {'id': 225, 'name': 'O15'}]
