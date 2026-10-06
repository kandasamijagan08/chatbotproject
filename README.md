# ai travel planner agent
                         ┌─────────────────────┐
                         │       USER          │
                         │ Destination, Budget │
                         │ Days, Interests     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    STREAMLIT UI     │
                         │   WanderDrop AI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────────┐
                  │       AI TRAVEL PLANNER         │
                  │                                 │
                  │  Research Agent                 │
                  │  Itinerary Agent                │
                  │  Budget Agent                   │
                  │  Hotel Agent                    │
                  │  Food Agent                     │
                  │  Transport Agent                │
                  │  Packing Agent                  │
                  │  Safety Agent                   │
                  └───────────────┬─────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
          ┌──────────────────┐        ┌──────────────────┐
          │ Hugging Face AI  │        │  Open-Meteo API  │
          │ DeepSeek Model   │        │ Weather & Geo    │
          └────────┬─────────┘        └────────┬─────────┘
                   │                           │
                   └─────────────┬─────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   SELF VERIFICATION    │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   COMPLETE TRAVEL PLAN │
                    │ Itinerary • Budget     │
                    │ Hotels • Food • Weather │
                    │ Transport • Safety     │
                    └────────────────────────┘
