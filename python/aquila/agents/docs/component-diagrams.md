
## Level 1: System Context Diagram

```mermaid
graph TD
    MP[Military Personnel] -->|Uses| MDAS[Military Decision Agent System]
    VFS[Video Feed System] -->|Provides video data| MDAS
    AIS[Audio Intercept System] -->|Provides audio data| MDAS
    IDB[Intelligence Database] -->|Provides textual reports| MDAS
    MDAS -->|Provides decision recommendations| MP
```

This diagram shows the high-level context of the Military Decision Agent System, including its interactions with users (Military Personnel) and external systems (Video Feed System, Audio Intercept System, and Intelligence Database).

## Level 2: Container Diagram

```mermaid
graph TD
    MP[Military Personnel] -->|Interacts with| WA[Web Application]
    WA -->|Sends requests| DEA[Decision Engine API]
    DEA -->|Processes video| VAS[Video Analysis Service]
    DEA -->|Processes audio| AAS[Audio Analysis Service]
    DEA -->|Processes text| TAS[Text Analysis Service]
    DEA -->|Integrates data| DIS[Data Integration Service]
    DEA -->|Evaluates ethics| EES[Ethical Evaluation Service]
    DEA -->|Stores/retrieves data| DB[(Database)]
    VFS[Video Feed System] -->|Provides video data| VAS
    AIS[Audio Intercept System] -->|Provides audio data| AAS
    IDB[Intelligence Database] -->|Provides textual reports| TAS
```

This diagram breaks down the Military Decision Agent System into its main containers, showing how they interact with each other and external systems.

## Level 3: Component Diagram (for Decision Engine API)

```mermaid
graph TD
    IP[Input Processor] -->|Sends data| PM[Perception Module]
    PM -->|Processed data| IM[Integration Module]
    IM -->|Integrated data| SAM[Situation Assessment Module]
    SAM -->|Situation analysis| COAG[Course of Action Generator]
    COAG -->|Proposed actions| EE[Ethical Evaluator]
    EE -->|Ethical assessment| DF[Decision Formulator]
    DF -->|Decision recommendation| OF[Output Formatter]
    
    VAS[Video Analysis Service] -->|Video analysis| PM
    AAS[Audio Analysis Service] -->|Audio analysis| PM
    TAS[Text Analysis Service] -->|Text analysis| PM
    
    EES[Ethical Evaluation Service] -->|Ethical guidelines| EE
    
    DB[(Database)] <-->|Data storage/retrieval| IP
    DB <-->|Data storage/retrieval| OF
```

This component diagram focuses on the Decision Engine API, showing how different modules within it interact to process inputs and generate decision recommendations.

These diagrams illustrate the growth loop and integration of the Military Decision Agent System, depicting key systems, actors, and relationships at different levels of abstraction.
