![Maintenance](https://img.shields.io/maintenance/no/2021)
![GitHub all releases](https://img.shields.io/github/downloads/khanxbahria/OWProxy/total)


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/khanxbahria/OWProxy">
    <img src="./gui/icon.ico" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">OWProxy</h3>

  <p align="center">
    An extensible TCP Proxy written for <a href="https://ourworld.com">ourWorld</a> with Outfit Mod & Shield.
    <br />
   <a href="#getting-started">Getting Started</a>




  </p>
</p>

<!-- PROJECT STATUS -->
## Project Status
This project is no longer maintained due to the game being shutdown on 16 Nov 2021.

<!-- ABOUT THE PROJECT -->
## About The Project
<p>
<img alt="OWProxy Screenshot" src="https://i.imgur.com/diZxGEyl.png" width=50% height=50%>
<img alt="OWProxy Screenshot" src="https://i.imgur.com/FmNk7Wnm.png"width=25% height=25%>
</p>


OWProxy is a custom TCP proxy to manipulate inbound and outbound payloads for ourWorld session.  
The functionality can be extended with custom plugins.  


<!-- GETTING STARTED -->
## Getting Started

## Windows
1. Download the latest Windows release here: [OWProxy for Windows](https://github.com/khanxbahria/OWProxy/releases/latest/download/OWProxy-win64.zip).
2. Extract the folder.
3. Before opening ourWorld client run OWProxy.exe


## Install from Source (Mac OS)

### Prerequisites

Download Python here: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation

1. Download the latest source release here: [OWProxy Source](https://github.com/khanxbahria/OWProxy/archive/refs/heads/main.zip).
2. Extract the folder.
3. Open terminal in the same folder, I am not going to teach you that.
  ```bash
  pip3 install -r requirements.txt
  ```
^ You need to do that just once.


<!-- USAGE EXAMPLES -->
## Usage

<img alt="OWProxy Mac Usage" src="https://i.imgur.com/pVgFppE.png" width=50% height=50%>

Before opening ourWorld client:  
  Open terminal in the same folder,
  ```bash 
  sudo python3 app.py
  ```  
To close OWProxy, exit the OWProxy window first before closing the terminal.

# Plugins

## Outfit

Lets you wear any possible outfit.
 To save the current outfit, edit the text inside the box and click save.
 A custom outfit can be made within user's Wishlist and selecting that as an option.
  ### outfits folder
  Outfits are loaded from and saved to outfits folder.  
  Additional outfits are added from jess's scripts into a subdirectory, outfits_old. You may choose to move them back to outfits folder to be able to use.

  ### Outfit Clone
  The **Dance off** button is mapped to clone that user's outfit. The dance request to that user is not sent, but their outfit is cloned on your avatar instead.


## Shield

This plugin blocks potentially malicious urls, allowing players to be protected from malicious session hijacking.  
All the loaded avatar images are replaced with NPC Edwin's image to protect the client from arbitrary code execution.

## Change Profile Color
![OWProxy Color Change](https://i.imgur.com/rtL9enWl.png)  
Change the color once the client is connected. You may have to restart the client for new color to be updated on your client.

### Disclaimer

  The code provided is as-is, and there are no guarantees that it fits your purposes.  
  The author shall not be liable for any damage to your account whether incurred directly or indirectly.  
  Use at your own risk.  
  

