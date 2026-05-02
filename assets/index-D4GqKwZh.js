import{r as c,R as e,m,c as u}from"./vendor-DFuypmeG.js";(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))r(a);new MutationObserver(a=>{for(const t of a)if(t.type==="childList")for(const i of t.addedNodes)i.tagName==="LINK"&&i.rel==="modulepreload"&&r(i)}).observe(document,{childList:!0,subtree:!0});function l(a){const t={};return a.integrity&&(t.integrity=a.integrity),a.referrerPolicy&&(t.referrerPolicy=a.referrerPolicy),a.crossOrigin==="use-credentials"?t.credentials="include":a.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function r(a){if(a.ep)return;a.ep=!0;const t=l(a);fetch(a.href,t)}})();function p({chart:n,id:s,theme:l}){const r=c.useRef(null);return c.useEffect(()=>{if(!r.current||!n)return;let a=!1;const t=l==="dark"?"dark":"neutral",i=`mermaid-diagram-${s}-${l}`;return m.initialize({startOnLoad:!1,theme:t}),m.render(i,n.trim()).then(({svg:o})=>{!a&&r.current&&(r.current.innerHTML=o)}).catch(o=>{console.error("Mermaid render error:",o),!a&&r.current&&(r.current.innerHTML=`<pre style="color:red;">Mermaid render failed: ${o.message}</pre>`)}),()=>{a=!0}},[n,s,l]),e.createElement("div",{ref:r,className:"mermaid-diagram"})}const d=["Home","Roadmap","Dashboard","Profile"],h=[{label:"Active Pods",value:"12",change:"+3 this month",icon:"🌿"},{label:"Avg Water pH",value:"7.1",change:"Stable",icon:"🧪"},{label:"Water Temp",value:"24°C",change:"Optimal",icon:"🌡️"},{label:"Ammonia",value:"0.02 ppm",change:"Safe",icon:"💧"},{label:"Plant Health",value:"92%",change:"+8% last week",icon:"🌱"},{label:"Light Cycle",value:"14h/day",change:"Active",icon:"💡"},{label:"Fish Activity",value:"Normal",change:"AI Monitored",icon:"🐟"},{label:"Energy Use",value:"A+",change:"Optimized",icon:"⚡"}],g=[{title:"Ecosystem Health Assessment",icon:"🩺",content:"Overall health is rated <strong>Excellent (95/100)</strong>. All key parameters are within optimal ranges. Fish are active, and plant growth is steady. No immediate concerns detected.",type:"assessment"},{title:"AI-driven Suggestion",icon:"🤖",content:"Ammonia levels have shown a slight upward trend over the past 48 hours. <strong>Recommendation:</strong> Reduce feeding amount by 10% for the next 3 days to maintain water quality.",type:"suggestion"},{title:"Upcoming Automation",icon:"⚙️",content:"The 'Sunrise' lighting schedule will activate in <strong>2 hours and 15 minutes</strong>, gradually increasing brightness to simulate a natural dawn for the plants and fish.",type:"automation"}],E=[{phase:"1. System Architecture Overview",detail:"Design a three-layer architecture including hardware, cloud services, and user applications. The hardware consists of modular EcoSphere pods with a master-slave structure, while the software is built on a modern stack with a monolithic backend, databases, and user-friendly web/app interfaces.",mermaid:`
flowchart LR
    subgraph HardwareSystem [Hardware System Architecture]
        subgraph ModularPods [EcoSphere Modular Pods]
            direction TB
            Master["Master Pod MCU (ESP32) <br> - WiFi/MQTT Uplink <br>- Local Network Coordinator"]
            Slave1["Slave Pod 1 (MCU)"]
            Slave2["Slave Pod 2 (MCU)"]
            
            Sensors["Sensors & Actuators Array"]
            
            Master <-->|BLE Mesh / I2C Pins| Slave1
            Master <-->|BLE Mesh / I2C Pins| Slave2
            Master --- Sensors
            Slave1 --- Sensors
        end
    end

    subgraph SoftwareSystem [Software System Architecture]
    direction TB
      subgraph CloudServer [Cloud / Server]
          direction TB
          APIGW["API Gateway <br> Nginx / Caddy"]
          Backend["Monolithic Backend Node.js / Python <br> - Core APIs<br>- Rule-based Engine<br>- Device Management"]
          DB[("Databases <br> - PostgreSQL + TimescaleDB<br>- Redis")]
          
          APIGW --> Backend
          Backend --> DB
      end

      subgraph UserLayer [User Layer]
          direction LR
          iOS["App <br> React Native"]
          Web["Web Dashboard <br> React / Vue"]
      end
    end
    
    iOS <-->|HTTPS / WebSocket| APIGW
    Web <-->|HTTPS / WebSocket| APIGW
    HardwareSystem <-->|MQTT / HTTP| SoftwareSystem
    `},{phase:"2. Embedded System Technical Solution",detail:"The embedded system uses an ESP32/STM32 MCU, integrating sensors (pH, temperature, etc.) and actuators (pumps, heaters). Communication is handled via WiFi and BLE Mesh, with a layered firmware architecture running on FreeRTOS for real-time data collection and control.",mermaid:`
flowchart TD
    subgraph "EcoSphere Pod Unit Hardware Design"
        direction TB
        subgraph MCULayer[MCU Layer]
            MCU[ESP32 / STM32 Cortex-M7]
        end
        subgraph SensorCollectionLayer[Sensor Collection Layer]
            Sensors[pH, Temp, DO, Light, etc.]
        end
        subgraph DriverControlLayer[Driver Control Layer]
            Drivers[Pumps, Heaters, LEDs, etc.]
        end
        subgraph CommunicationLayer[Communication Layer]
            Comm[WiFi, BLE Mesh, I2C]
        end
        
        Sensors -->|Data| MCU
        MCU -->|Control| Drivers
        MCU <-->|Comm| Comm
    end
    `},{phase:"3. Backend Services & Database Design",detail:"A monolithic backend using Node.js/Python provides RESTful APIs for user, pod, and data management. It features a rule engine for automation. Data is stored in PostgreSQL with TimescaleDB for time-series data and Redis for caching.",mermaid:`
flowchart TD
    Gateway[Web Server Nginx / Caddy]
    
    subgraph MonolithicBackendApp[Monolithic Backend App]
        API[Express.js / FastAPI App]
        User[User Module]
        Pod[Pod & Device Module]
        Rule[Rule Engine]
        
        API --> User & Pod & Rule
    end
    
    subgraph StorageLayer[Storage Layer]
        PG[(PostgreSQL + TimescaleDB)]
        Redis[(Redis Cache)]
        S3[(MinIO Object Storage)]
    end
    
    Gateway --> API
    API --> PG & Redis & S3
    `},{phase:"4. Data & AI Technical Solution",detail:"The initial data pipeline relies on MQTT for data collection, processed by the backend and stored. The MVP intelligence uses expert systems and statistical models for anomaly detection and automated interventions, deferring complex ML models until sufficient data is collected.",mermaid:`
flowchart TD
    subgraph DCL[Data Collection Layer]
        IoT[Master Pod MQTT & HTTP]
    end
    
    Broker[MQTT Broker]
    API[Backend API]
    
    DCL --> Broker --> API
    
    API --> DB_SQL[(Hypertable / Postgres)]
    API --> ObjectDB[(MinIO / S3)]
    
    DB_SQL --> Cron[CRON Jobs / Aggregation]
    Cron --> Rules[Statistical Thresholds]
    
    Rules --> Push[App Alerts]
    `},{phase:"5. System Integration & Interfaces",detail:"Embedded devices communicate with the cloud via MQTT over secure WiFi. The frontend (Web/App) interacts with the backend through REST APIs and WebSockets for real-time updates, ensuring a seamless user experience for monitoring and controlling the EcoSphere pods."}];function b(){const[n,s]=c.useState("Home"),[l,r]=c.useState("light"),a=c.useMemo(()=>l==="light"?"Switch to Dark":"Switch to Light",[l]);return e.createElement("div",{className:`app theme-${l}`},e.createElement("div",{className:"ambient ambient-1"}),e.createElement("div",{className:"ambient ambient-2"}),e.createElement("header",{className:"topbar glass"},e.createElement("div",{className:"brand-group"},e.createElement("h1",null,"EcoSphere Pod"),e.createElement("div",{className:"brand-tagline"},e.createElement("p",null,"SEA-CICSIC 2026 Project Demo"),e.createElement("p",null,"Modular Living Ecosystem Platform"))),e.createElement("div",{className:"actions"},e.createElement("button",{className:"theme-toggle",onClick:()=>r(l==="light"?"dark":"light")},a))),e.createElement("nav",{className:"tabs glass","aria-label":"Main tabs"},e.createElement("div",{className:"tab-section tab-left"},d.slice(0,2).map(t=>e.createElement("button",{key:t,className:`tab-btn ${n===t?"active":""}`,onClick:()=>s(t)},t)),e.createElement("div",{className:"tab-divider divider-public"},e.createElement("span",{className:"divider-content"},"✦ Public"))),e.createElement("div",{className:"tab-divider-center"},e.createElement("span",{className:"divider-content"},"✦ Public")," ",e.createElement("span",{className:"divider-line"},"|")," ",e.createElement("span",{className:"divider-content"},"Private ✦")),e.createElement("div",{className:"tab-section tab-right"},d.slice(2).map(t=>e.createElement("button",{key:t,className:`tab-btn ${n===t?"active":""}`,onClick:()=>s(t)},t)),e.createElement("div",{className:"tab-divider divider-private"},e.createElement("span",{className:"divider-content"},"✦ Private")))),e.createElement("main",{className:"content"},n==="Home"&&e.createElement("section",{className:"panel fade-in"},e.createElement("h2",null,"Home"),e.createElement("p",null,"Welcome to the Future of Sustainable Living."),e.createElement("div",{className:"home-grid"},e.createElement("article",{className:"home-tile glass"},e.createElement("h3",null,"Introduction"),e.createElement("p",null,"The EcoSphere Pod project re-imagines aquaponics, transforming it from a bulky, static farming system into a modular, intelligent, and beautiful living ecosystem. It's a portable, scalable solution designed for modern urban lifestyles, integrating IoT and AI to create self-sustaining environments.")),e.createElement("article",{className:"home-tile glass"},e.createElement("h3",null,"The Big Concept: ECO-SPHERE POD"),e.createElement("p",null,"A modular smart ecosystem combining fish, plants, water circulation, sensors, and AI monitoring. Pods connect like LEGOs, allowing you to create anything from a single decorative piece to a full-scale urban micro-farm. The system is built on a robust three-layer architecture: Embedded, Backend, and Frontend.")),e.createElement("article",{className:"home-tile glass"},e.createElement("h3",null,"Example Use Cases"),e.createElement("div",{className:"use-cases"},e.createElement("div",{className:"use-case"},e.createElement("span",{className:"use-case-icon"},"🏠"),e.createElement("p",null,e.createElement("strong",null,"Home/Office Decoration:")," A beautiful, self-sustaining aquarium-plant feature that also grows fresh herbs.")),e.createElement("div",{className:"use-case"},e.createElement("span",{className:"use-case-icon"},"🏙️"),e.createElement("p",null,e.createElement("strong",null,"Urban Food Production:")," Stack pods to grow vegetables and greens in apartments with limited space.")),e.createElement("div",{className:"use-case"},e.createElement("span",{className:"use-case-icon"},"🎓"),e.createElement("p",null,e.createElement("strong",null,"Educational Tool:")," An interactive way for schools to teach about ecosystems, biology, and technology.")),e.createElement("div",{className:"use-case"},e.createElement("span",{className:"use-case-icon"},"🚀"),e.createElement("p",null,e.createElement("strong",null,"Future Habitats:")," A visionary concept for self-sufficient, closed-loop ecosystems in extreme environments.")))),e.createElement("article",{className:"home-tile glass"},e.createElement("h3",null,"Key Features"),e.createElement("ul",null,e.createElement("li",null,e.createElement("strong",null,"Modular Design:")," Stackable pods for customized setups."),e.createElement("li",null,e.createElement("strong",null,"Real-time Monitoring:")," Live data on water quality, temperature, and more."),e.createElement("li",null,e.createElement("strong",null,"AI-Powered Automation:")," Automated adjustments for a stable environment."),e.createElement("li",null,e.createElement("strong",null,"Remote Control:")," Manage your ecosystem from anywhere via web or mobile app."),e.createElement("li",null,e.createElement("strong",null,"Sustainable:")," Low energy use and efficient water circulation."))))),n==="Dashboard"&&e.createElement("section",{className:"panel fade-in"},e.createElement("h2",null,"Dashboard"),e.createElement("p",null,"Live ecosystem snapshot with sustainability-oriented operational metrics."),e.createElement("div",{className:"dashboard-grid"},e.createElement("div",{className:"cards-container"},h.map(t=>e.createElement("article",{key:t.label,className:"card glass"},e.createElement("div",{className:"card-header"},e.createElement("span",{className:"card-icon"},t.icon),e.createElement("p",{className:"card-label"},t.label)),e.createElement("p",{className:"card-value"},t.value),e.createElement("p",{className:"card-change"},t.change)))),e.createElement("div",{className:"video-feed-placeholder glass"},e.createElement("div",{className:"placeholder-content"},e.createElement("span",{className:"video-icon"},"📹"),e.createElement("h3",null,"Live Fish Cam"),e.createElement("p",null,"Video feed from Pod #1")))),e.createElement("div",{className:"insights-container"},g.map(t=>e.createElement("article",{key:t.title,className:`insight-card glass ${t.type}`},e.createElement("div",{className:"card-header"},e.createElement("span",{className:"card-icon"},t.icon),e.createElement("h3",{className:"card-label"},t.title)),e.createElement("p",{className:"card-content",dangerouslySetInnerHTML:{__html:t.content}}))))),n==="Roadmap"&&e.createElement("section",{className:"panel fade-in"},e.createElement("h2",null,"Technical Roadmap"),e.createElement("p",null,"Step-by-step technical development plan for the EcoSphere Pod project."),e.createElement("div",{className:"roadmap-timeline"},E.map((t,i)=>e.createElement("div",{key:i,className:"roadmap-item glass"},e.createElement("div",{className:"roadmap-header"},e.createElement("h3",null,t.phase)),e.createElement("p",null,t.detail),t.mermaid&&e.createElement(p,{chart:t.mermaid,id:i,theme:l}))))),n==="Profile"&&e.createElement("section",{className:"panel fade-in"},e.createElement("h2",null,"Profile"),e.createElement("p",null,"Manage your account, settings, and connected EcoSphere Pods."),e.createElement("div",{className:"profile-grid"},e.createElement("article",{className:"profile-card glass"},e.createElement("h3",null,"User Information"),e.createElement("div",{className:"user-info"},e.createElement("div",{className:"avatar"},"👤"),e.createElement("div",{className:"user-details"},e.createElement("p",null,e.createElement("strong",null,"Name:")," Alex Doe"),e.createElement("p",null,e.createElement("strong",null,"Email:")," alex.doe@example.com"),e.createElement("p",null,e.createElement("strong",null,"Member Since:")," Jan 2026"),e.createElement("button",{className:"profile-button"},"Edit Profile")))),e.createElement("article",{className:"profile-card glass"},e.createElement("h3",null,"Notification Settings"),e.createElement("div",{className:"settings-group"},e.createElement("div",{className:"setting-item"},e.createElement("label",{htmlFor:"alert-toggle"},"Critical Alerts"),e.createElement("input",{type:"checkbox",id:"alert-toggle",defaultChecked:!0})),e.createElement("div",{className:"setting-item"},e.createElement("label",{htmlFor:"suggestion-toggle"},"AI Suggestions"),e.createElement("input",{type:"checkbox",id:"suggestion-toggle",defaultChecked:!0})),e.createElement("div",{className:"setting-item"},e.createElement("label",{htmlFor:"report-toggle"},"Weekly Reports"),e.createElement("input",{type:"checkbox",id:"report-toggle"})),e.createElement("button",{className:"profile-button"},"Save Settings"))),e.createElement("article",{className:"profile-card glass"},e.createElement("h3",null,"My EcoSphere Pods"),e.createElement("div",{className:"device-list"},e.createElement("div",{className:"device-item"},e.createElement("p",null,"Living Room Pod 🌿"),e.createElement("span",null,"Online")),e.createElement("div",{className:"device-item"},e.createElement("p",null,"Kitchen Herb Garden 🌱"),e.createElement("span",null,"Online")),e.createElement("div",{className:"device-item"},e.createElement("p",null,"Bedroom Pod 🔌"),e.createElement("span",null,"Offline")),e.createElement("button",{className:"profile-button"},"Manage Devices")))))))}u(document.getElementById("root")).render(e.createElement(e.StrictMode,null,e.createElement(b,null)));
