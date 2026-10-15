"""
Viral Script Generator & Metadata Engine
Optimized for 80%+ Audience Retention, Loop Closures, and YouTube 2026 AI Policy Compliance.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class VideoScript:
    topic_id: str
    niche: str
    title: str
    language: str
    hook: str
    story_chunks: List[str]
    loop_close: str
    full_narration: str
    tags: List[str]
    description: str
    estimated_duration_sec: int
    category_id: str = "28"  # Science & Technology
    contains_synthetic_media: bool = True  # YouTube 2026 Policy Flag

VIRAL_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "y2k38_bug": {
        "niche": "Mind-Bending Tech Mysteries",
        "title": "19 January 2038: The Day Internet Might Die! ⚠️ #Shorts",
        "language": "hi",
        "hook": "Duniya bhar ke banks aur servers 19 January 2038 ko achanak crash ho sakte hain!",
        "story_chunks": [
            "Aur iski wajah koi nuclear war ya solar flare nahi, balki code ki sirf ek chhoti si limit hai.",
            "Ise kehte hain Year 2038 Problem ya Unix Epoch Bug.",
            "Aaj bhi duniya ke 80% critical servers 32-bit signed integer par time count karte hain.",
            "Yeh counter 1 January 1970 se shuru hua tha aur iski aakhri limit hai 2,147,483,647 seconds.",
            "Jaise hi 19 January 2038 ko 3 bajkar 14 minute honge, yeh number overflow ho jayega aur time 1901 me chala jayega!",
            "Flight systems, stock markets aur banking transactions turant freeze ho jayenge.",
            "Engineers din raat ise 64-bit me migrate kar rahe hain, par agar ek bhi system bacha, toh tabahi pakki hai."
        ],
        "loop_close": "Aur yahi wajah hai ki...",
        "tags": ["Y2K38", "TechMysteries", "CodingFacts", "UnixBug", "ComputerScience", "DarkTech", "Shorts", "ViralFacts"],
        "description": "Kya 2038 me duniya ka saara internet freeze ho jayega? Janie Unix Epoch 32-bit integer overflow bug ki poori sachai.\n\n🔔 Subscribe for mind-bending tech paradoxes & engineering mysteries.\n\n#Shorts #TechMysteries #Coding #ComputerScience #Technology"
    },
    "undersea_cables": {
        "niche": "Dark Infrastructure",
        "title": "99% Internet Samundar Ke Niche Chhupa Hai! 🌊🌐 #Shorts",
        "language": "hi",
        "hook": "Aap jo yeh video dekh rahe ho, yeh kisi satellite se nahi, samundar ki gahraiyon se aa rahi hai!",
        "story_chunks": [
            "Log sochte hain internet space satellite se chalta hai, par 99% global data samundar ke niche bichi patli fiber-optic cables se guzarta hai.",
            "Puri duniya me aisi 500 se zyada submarine cables hain jo 1.4 million kilometers lambi hain.",
            "Yeh cables sirf ek garden hose jitni patli hoti hain, par inme lakho terabytes per second speed hoti hai.",
            "Khatra yeh hai ki agar kisi submarine ya undersea earthquake ne sirf 5 major cable points kaat diye, toh poore continents offline ho jayenge aur global economy ghanto me collapse ho jayegi."
        ],
        "loop_close": "Agli baar jab aap internet connect karein, yaad rakhna...",
        "tags": ["InternetInfrastructure", "UnderseaCables", "TechSecrets", "SubmarineCable", "Shorts", "Facts"],
        "description": "Satellite nahi, 99% Internet samundar ke niche chal raha hai! Submarine fiber-optic cables ki hidden reality.\n\n#Shorts #TechFacts #Internet #Engineering"
    },
    "stuxnet_virus": {
        "niche": "Cyber Warfare",
        "title": "The Invisible Weapon That Blew Up A Nuclear Plant ☢️💻 #Shorts",
        "language": "hi",
        "hook": "Bina ek bhi goli chalaye, ek invisible computer virus ne ek poori nuclear facility blast kar di!",
        "story_chunks": [
            "Year 2010 me Iran ki sabse secure Natanz nuclear facility achanak phatne lagi.",
            "Unke ultra-speed uranium centrifuges out of control ghoom kar khud ko tod rahe the, par computer screens sab normal dikha rahi thi.",
            "Pata chala wahan duniya ka sabse lethal digital weapon ghoosa tha — Stuxnet.",
            "Yeh virus internet se nahi, balki ek contaminated USB drive ke zariye air-gapped system me inject kiya gaya tha.",
            "Isne history me pehli baar digital code se physical machine ko tabah karke dikha diya."
        ],
        "loop_close": "Aur tab se duniya ki cyber warfare badal gayi, kyunki...",
        "tags": ["Stuxnet", "CyberSecurity", "NuclearMystery", "DarkTech", "HackingFacts", "Shorts"],
        "description": "Kaise ek 500 KB ke code ne Iran ki nuclear plant centrifuge ko blast kar diya? The story of Stuxnet.\n\n#Shorts #CyberSecurity #Stuxnet #Hacking"
    }
}

class ScriptGenerator:
    """Generates viral, retention-engineered scripts tailored for YouTube Shorts."""

    @staticmethod
    def get_template(topic_id: str = "y2k38_bug") -> VideoScript:
        if topic_id not in VIRAL_TEMPLATES:
            topic_id = "y2k38_bug"
        
        data = VIRAL_TEMPLATES[topic_id]
        
        # Assemble full narration with natural pauses
        full_text = f"{data['hook']} {' '.join(data['story_chunks'])} {data['loop_close']}"
        word_count = len(full_text.split())
        # Average speaking tempo: 2.7 words/sec
        estimated_duration = max(25, int(word_count / 2.7))
        
        return VideoScript(
            topic_id=topic_id,
            niche=data["niche"],
            title=data["title"],
            language=data["language"],
            hook=data["hook"],
            story_chunks=data["story_chunks"],
            loop_close=data["loop_close"],
            full_narration=full_text,
            tags=data["tags"],
            description=data["description"],
            estimated_duration_sec=estimated_duration
        )

    @staticmethod
    def create_custom_script(
        topic: str,
        hook: str,
        points: List[str],
        loop_phrase: str,
        language: str = "hi"
    ) -> VideoScript:
        full_text = f"{hook} {' '.join(points)} {loop_phrase}"
        word_count = len(full_text.split())
        estimated_duration = max(25, int(word_count / 2.7))
        
        title = f"{topic[:50]}! 🤯 #Shorts"
        tags = ["Shorts", "Facts", "TechFacts", "ViralShorts", "Trending", "Knowledge"]
        description = f"{topic}\n\nEducational breakdown & facts.\n\n#Shorts #Facts #Knowledge"
        
        return VideoScript(
            topic_id="custom",
            niche="Custom Viral Niche",
            title=title,
            language=language,
            hook=hook,
            story_chunks=points,
            loop_close=loop_phrase,
            full_narration=full_text,
            tags=tags,
            description=description,
            estimated_duration_sec=estimated_duration
        )

    @staticmethod
    def list_available_templates() -> List[Dict[str, str]]:
        return [
            {"id": k, "title": v["title"], "niche": v["niche"]}
            for k, v in VIRAL_TEMPLATES.items()
        ]
