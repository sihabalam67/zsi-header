# Playbook: run the whole agency

Six roles in order, from a blank page to a niche, a first video and a monetization plan. Each step feeds the next, so the agent carries the shortlist, the winning niche and the outliers forward.

| Step | Role | Skill | Prompt to paste | You get |
|---|---|---|---|---|
| 1 | 🔭 Niche scout | `niche-finder` | "Find me unsaturated niche ideas in English with real money in them, ranked." | ten ranked niche ideas, each with proof and a way to earn beyond AdSense |
| 2 | ⚖️ Validator | `niche-validator` | "Validate the top three ideas from the shortlist. Compare them, then give me the full verdict for the strongest." | a comparison table of the three, then scores, verdict, channels breaking in, formats, gaps and an entry plan for the winner |
| 3 | 📈 Trend analyst | `trend-report` | "Trend report for the winning niche this month. Hooks word for word." | the videos winning now, with verbatim hooks and why they worked, patterns and ideas |
| 4 | 🎬 Script analyst | `script-breakdown` | "Break down the two strongest outliers from the trend report, and give me a script skeleton for the first video." | hooks verbatim, typed beats with timestamps, a shared layout and a skeleton |
| 5 | 🎨 Packaging team | `title-formulas`, then `thumbnail-concepts` | "Give me a title and a thumbnail for that first video." | about eight titles with proof, then three thumbnail concepts for the chosen title, with images or prompts |
| 6 | 💰 Monetization team | `revenue-maxxing` | "What do channels in this niche sell, and who sponsors them?" | a stack score across ad revenue, sponsors, buyer intent, a newsletter and own products, with monetization gaps, sponsors and the moves in build order |

In Claude Code with the plugin installed, each step can go to its agent: `@agent-youtube-research:niche-scout`, `@agent-youtube-research:validator`, and so on down the roles. Steps that do not need each other, such as the trend report and the monetization plan once the niche is chosen, can run at the same time. An agent does not see the chat, so each request should name the niche and any outliers it builds on. On other clients, run the prompts in order in one chat.

Rules the chain relies on: `classificationQuality: "neutral"` throughout, and `"positive"` for the thumbnail in step 5. Every number comes from a tool response. Everything cited is linked with a URL from tool data: videos, channels, moments, brands and products. A sponsor that was only heard links to the video moment. Estimates are bands. If a step says "thin signal", go back one step rather than forcing it.
