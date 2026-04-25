import React, { useMemo, useState, useEffect, useRef, useCallback } from "react";
import mermaid from "mermaid";

function MermaidDiagram({ chart, id, theme }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || !chart) return;
    let cancelled = false;
    const mermaidTheme = theme === 'dark' ? 'dark' : 'neutral';
    const diagramId = `mermaid-diagram-${id}-${theme}`;

    mermaid.initialize({ startOnLoad: false, theme: mermaidTheme });

    mermaid.render(diagramId, chart.trim()).then(({ svg }) => {
      if (!cancelled && containerRef.current) {
        containerRef.current.innerHTML = svg;
      }
    }).catch((err) => {
      console.error('Mermaid render error:', err);
      if (!cancelled && containerRef.current) {
        containerRef.current.innerHTML = `<pre style="color:red;">Mermaid render failed: ${err.message}</pre>`;
      }
    });

    return () => { cancelled = true; };
  }, [chart, id, theme]);

  return <div ref={containerRef} className="mermaid-diagram" />;
}

const tabs = ["Home", "Dashboard", "Roadmap", "Profile"];

const statCards = [
  { label: "Active Pods", value: "12", change: "+3 this month", icon: "🌿" },
  { label: "Avg Water pH", value: "7.1", change: "Stable", icon: "🧪" },
  { label: "Water Temp", value: "24°C", change: "Optimal", icon: "🌡️" },
  { label: "Ammonia", value: "0.02 ppm", change: "Safe", icon: "💧" },
  { label: "Plant Health", value: "92%", change: "+8% last week", icon: "🌱" },
  { label: "Light Cycle", value: "14h/day", change: "Active", icon: "💡" },
  { label: "Fish Activity", value: "Normal", change: "AI Monitored", icon: "🐟" },
  { label: "Energy Use", value: "A+", change: "Optimized", icon: "⚡" }
];

const insightCards = [
  {
    title: "Ecosystem Health Assessment",
    icon: "🩺",
    content: "Overall health is rated <strong>Excellent (95/100)</strong>. All key parameters are within optimal ranges. Fish are active, and plant growth is steady. No immediate concerns detected.",
    type: "assessment"
  },
  {
    title: "AI-driven Suggestion",
    icon: "🤖",
    content: "Ammonia levels have shown a slight upward trend over the past 48 hours. <strong>Recommendation:</strong> Reduce feeding amount by 10% for the next 3 days to maintain water quality.",
    type: "suggestion"
  },
  {
    title: "Upcoming Automation",
    icon: "⚙️",
    content: "The 'Sunrise' lighting schedule will activate in <strong>2 hours and 15 minutes</strong>, gradually increasing brightness to simulate a natural dawn for the plants and fish.",
    type: "automation"
  }
];

const roadmapItems = [
  {
    phase: "1. System Architecture Overview",
    detail: "Design a three-layer architecture including hardware, cloud services, and user applications. The hardware consists of modular EcoSphere pods with a master-slave structure, while the software is built on a modern stack with a monolithic backend, databases, and user-friendly web/app interfaces.",
    mermaid: `
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
    `
  },
  {
    phase: "2. Embedded System Technical Solution",
    detail: "The embedded system uses an ESP32/STM32 MCU, integrating sensors (pH, temperature, etc.) and actuators (pumps, heaters). Communication is handled via WiFi and BLE Mesh, with a layered firmware architecture running on FreeRTOS for real-time data collection and control.",
    mermaid: `
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
    `
  },
  {
    phase: "3. Backend Services & Database Design",
    detail: "A monolithic backend using Node.js/Python provides RESTful APIs for user, pod, and data management. It features a rule engine for automation. Data is stored in PostgreSQL with TimescaleDB for time-series data and Redis for caching.",
    mermaid: `
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
    `
  },
  {
    phase: "4. Data & AI Technical Solution",
    detail: "The initial data pipeline relies on MQTT for data collection, processed by the backend and stored. The MVP intelligence uses expert systems and statistical models for anomaly detection and automated interventions, deferring complex ML models until sufficient data is collected.",
    mermaid: `
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
    `
  },
  {
    phase: "5. System Integration & Interfaces",
    detail: "Embedded devices communicate with the cloud via MQTT over secure WiFi. The frontend (Web/App) interacts with the backend through REST APIs and WebSockets for real-time updates, ensuring a seamless user experience for monitoring and controlling the EcoSphere pods."
  }
];

function App() {
  const [activeTab, setActiveTab] = useState("Home");
  const [theme, setTheme] = useState("light");


  const themeLabel = useMemo(
    () => (theme === "light" ? "Switch to Dark" : "Switch to Light"),
    [theme]
  );

  return (
    <div className={`app theme-${theme}`}>
      <div className="ambient ambient-1" />
      <div className="ambient ambient-2" />

      <header className="topbar glass">
        <div className="brand-group">
          <h1>EcoSphere Pod</h1>
          <div className="brand-tagline">
            <p>SEA-CICSIC 2026 Project Demo</p>
            <p>Modular Living Ecosystem Platform</p>
          </div>
        </div>

        <div className="actions">
          <button
            className="theme-toggle"
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          >
            {themeLabel}
          </button>
        </div>
      </header>

      <nav className="tabs glass" aria-label="Main tabs">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`tab-btn ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      <main className="content">
        {activeTab === "Home" && (
          <section className="panel fade-in">
            <h2>Home</h2>
            <p>
              Welcome to the Future of Sustainable Living.
            </p>
            <div className="home-grid">
              <article className="home-tile glass">
                <h3>Introduction</h3>
                <p>
                  The EcoSphere Pod project re-imagines aquaponics, transforming it from a bulky, static farming system into a modular, intelligent, and beautiful living ecosystem. It's a portable, scalable solution designed for modern urban lifestyles, integrating IoT and AI to create self-sustaining environments.
                </p>
              </article>

              <article className="home-tile glass">
                <h3>The Big Concept: ECO-SPHERE POD</h3>
                <p>
                  A modular smart ecosystem combining fish, plants, water circulation, sensors, and
                  AI monitoring. Pods connect like LEGOs, allowing you to create anything from a
                  single decorative piece to a full-scale urban micro-farm. The system is built on a robust three-layer architecture: Embedded, Backend, and Frontend.
                </p>
              </article>

              <article className="home-tile glass">
                <h3>Example Use Cases</h3>
                <div className="use-cases">
                  <div className="use-case">
                    <span className="use-case-icon">🏠</span>
                    <p>
                      <strong>Home/Office Decoration:</strong> A beautiful, self-sustaining
                      aquarium-plant feature that also grows fresh herbs.
                    </p>
                  </div>
                  <div className="use-case">
                    <span className="use-case-icon">🏙️</span>
                    <p>
                      <strong>Urban Food Production:</strong> Stack pods to grow vegetables and
                      greens in apartments with limited space.
                    </p>
                  </div>
                  <div className="use-case">
                    <span className="use-case-icon">🎓</span>
                    <p>
                      <strong>Educational Tool:</strong> An interactive way for schools to teach
                      about ecosystems, biology, and technology.
                    </p>
                  </div>
                  <div className="use-case">
                    <span className="use-case-icon">🚀</span>
                    <p>
                      <strong>Future Habitats:</strong> A visionary concept for self-sufficient,
                      closed-loop ecosystems in extreme environments.
                    </p>
                  </div>
                </div>
              </article>

              <article className="home-tile glass">
                <h3>Key Features</h3>
                <ul>
                  <li><strong>Modular Design:</strong> Stackable pods for customized setups.</li>
                  <li><strong>Real-time Monitoring:</strong> Live data on water quality, temperature, and more.</li>
                  <li><strong>AI-Powered Automation:</strong> Automated adjustments for a stable environment.</li>
                  <li><strong>Remote Control:</strong> Manage your ecosystem from anywhere via web or mobile app.</li>
                  <li><strong>Sustainable:</strong> Low energy use and efficient water circulation.</li>
                </ul>
              </article>
            </div>
          </section>
        )}

        {activeTab === "Dashboard" && (
          <section className="panel fade-in">
            <h2>Dashboard</h2>
            <p>Live ecosystem snapshot with sustainability-oriented operational metrics.</p>
            <div className="dashboard-grid">
              <div className="cards-container">
                {statCards.map((card) => (
                  <article key={card.label} className="card glass">
                    <div className="card-header">
                      <span className="card-icon">{card.icon}</span>
                      <p className="card-label">{card.label}</p>
                    </div>
                    <p className="card-value">{card.value}</p>
                    <p className="card-change">{card.change}</p>
                  </article>
                ))}
              </div>
              <div className="video-feed-placeholder glass">
                <div className="placeholder-content">
                  <span className="video-icon">📹</span>
                  <h3>Live Fish Cam</h3>
                  <p>Video feed from Pod #1</p>
                </div>
              </div>
            </div>
            <div className="insights-container">
              {insightCards.map((card) => (
                <article key={card.title} className={`insight-card glass ${card.type}`}>
                  <div className="card-header">
                    <span className="card-icon">{card.icon}</span>
                    <h3 className="card-label">{card.title}</h3>
                  </div>
                  <p className="card-content" dangerouslySetInnerHTML={{ __html: card.content }} />
                </article>
              ))}
            </div>
          </section>
        )}

        {activeTab === "Roadmap" && (
          <section className="panel fade-in">
            <h2>Technical Roadmap</h2>
            <p>Step-by-step technical development plan for the EcoSphere Pod project.</p>
            <div className="roadmap-timeline">
              {roadmapItems.map((item, index) => (
                <div key={index} className="roadmap-item glass">
                  <div className="roadmap-header">
                    <h3>{item.phase}</h3>
                  </div>
                  <p>{item.detail}</p>
                  {item.mermaid && (
                    <MermaidDiagram chart={item.mermaid} id={index} theme={theme} />
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === "Profile" && (
          <section className="panel fade-in">
            <h2>Profile</h2>
            <p>Manage your account, settings, and connected EcoSphere Pods.</p>
            <div className="profile-grid">
              <article className="profile-card glass">
                <h3>User Information</h3>
                <div className="user-info">
                  <div className="avatar">👤</div>
                  <div className="user-details">
                    <p><strong>Name:</strong> Alex Doe</p>
                    <p><strong>Email:</strong> alex.doe@example.com</p>
                    <p><strong>Member Since:</strong> Jan 2026</p>
                    <button className="profile-button">Edit Profile</button>
                  </div>
                </div>
              </article>

              <article className="profile-card glass">
                <h3>Notification Settings</h3>
                <div className="settings-group">
                  <div className="setting-item">
                    <label htmlFor="alert-toggle">Critical Alerts</label>
                    <input type="checkbox" id="alert-toggle" defaultChecked />
                  </div>
                  <div className="setting-item">
                    <label htmlFor="suggestion-toggle">AI Suggestions</label>
                    <input type="checkbox" id="suggestion-toggle" defaultChecked />
                  </div>
                  <div className="setting-item">
                    <label htmlFor="report-toggle">Weekly Reports</label>
                    <input type="checkbox" id="report-toggle" />
                  </div>
                  <button className="profile-button">Save Settings</button>
                </div>
              </article>

              <article className="profile-card glass">
                <h3>My EcoSphere Pods</h3>
                <div className="device-list">
                  <div className="device-item">
                    <p>Living Room Pod 🌿</p>
                    <span>Online</span>
                  </div>
                  <div className="device-item">
                    <p>Kitchen Herb Garden 🌱</p>
                    <span>Online</span>
                  </div>
                  <div className="device-item">
                    <p>Bedroom Pod 🔌</p>
                    <span>Offline</span>
                  </div>
                  <button className="profile-button">Manage Devices</button>
                </div>
              </article>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
