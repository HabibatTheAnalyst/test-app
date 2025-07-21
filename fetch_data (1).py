import os
import json
from typing import Dict, Any
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

# SEO templates for all country chart types
seo_templates = {
    "key stats": {
        "SEO-title":
        "{country}'s government Key Stats table",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Key statistics table displaying core political and economic data, including key indicators such as population, GDP, government structure, and democracy metrics in {country}.",
        "SEO-description":
        "Explore {country}'s core political and economic data through an informative table detailing key indicators, such as population, GDP, government structure, and democracy metrics. This table pr[...]",
        "SEO-keywords": [
            "{country} government information", "{country} political data",
            "{country} economic data", "{country} key indicators",
            "{country} population data", "{country} GDP",
            "{country} government structure", "{country} president age",
            "{country} president tenure", "{country} military regime status",
            "{country} democracy metrics",
            "{country} political and economic overview",
            "{country} leadership indicators", "{country} governance metrics",
            "{country} democracy status", "{country} core political data",
            "{country} economic data", "{country} governance landscape",
            "{country} development landscape",
            "{country} system of government", "{country} government structure",
            "{country} democracy level", "{country} leadership details",
            "{country} legislative structure",
            "{country} position in African governance",
            "{country} democratic evolution", "When is {country} election?",
            "When will {country} elect president?", "{country} democracy",
            "{country} election", "{country} democratic history",
            "{country} history since independence",
            "{country} democracy rating", "{country} democracy score"
        ]
    },
    "democratic history": {
        "SEO-title":
        "{country} Historical and political timeline",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "History timeline table outlining significant political and economic events, highlighting major milestones such as independence, regime changes, economic reforms, coup, and key developments an[...]",
        "SEO-description":
        "Explore {country}'s rich historical timeline through a detailed table, covering milestones such as {country}'s independence date, referendum history, and pivotal events. This table provides e[...]",
        "SEO-keywords": [
            "{country} historical timeline", "political milestones {country}",
            "{country} independence history", "{country} referendum history",
            "coups in {country}", "notable wars in {country}",
            "assassinations in {country}", "fight for freedom in {country}",
            "{country} political development",
            "governance changes in {country}", "{country} democracy journey",
            "{country} African governance history",
            "modern political history {country}", "landmark events {country}",
            "{country} path to independence",
            "shifts in political power {country}",
            "{country} historical governance", "political evolution {country}",
            "key events {country} political history", "{country} democracy",
            "{country} election", "{country} democratic history",
            "{country} history since independence",
            "{country} democracy rating", "{country} democracy score"
        ]
    },
    "candidates": {
        "SEO-title":
        "{country} {year} presidential Candidates",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Candidate chart displaying the {year} {country} presidential candidates, with key data covering their background, political alignment, and government experience.",
        "SEO-description":
        "Explore detailed information on {country}'s presidential candidates, with key data covering their background, political alignment, and government experience. This table provides essential ins[...]",
        "SEO-keywords": [
            "{country} presidential candidates", "{country} election",
            "{country} political parties", "Presidential candidates biography",
            "Presidential candidates profile",
            "Presidential candidates background",
            "Presidential candidates political career",
            "{country} election results {year}", "{country} political history",
            "{country} governance", "{country} democracy",
            "{country} leadership", "{country} government structure",
            "{country} political landscape", "{country} elections",
            "{country} political system", "{country} presidential candidate",
            "Who is running for {country} president?",
            "When is {country} election?",
            "When will {country} elect president?"
        ]
    },
    "parliament": {
        "SEO-title":
        "{country} {year} parliament chart",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Interactive parliamentary election chart displaying the {year} {country} parliamentary election results, illustrating the distribution of seats by political parties.",
        "SEO-description":
        "Explore detailed charts on {country}'s parliamentary election results, with number of seats broken down by political parties across election years. These visualizations provide essential insi[...]",
        "SEO-keywords": [
            "{country} parliamentary election results",
            "{country} election results by party",
            "political party performance {country}",
            "{country} election trends", "voter shifts {country} elections",
            "political party shifts {country}", "{country} election charts",
            "{country} parliamentary seats by party",
            "election trends in {country}", "African elections analysis",
            "{country} democracy analysis", "{country} election data",
            "{country} voter trends", "{country} election performance",
            "{country} political party analysis", "{country} democracy trends",
            "election years in {country}", "{country} political party results",
            "{country} elections voter shifts",
            "African parliamentary elections", "When is {country} election?",
            "When will {country} elect president?",
            "Who won {country} election?", "Who won {country} president?",
            "Which party won {country}?", "{country} parliament results",
            "{country} legislative control",
            "number of seats by political parties",
            "parliamentary election trends in {country}",
            "{country} political landscape", "African elections",
            "{country} democracy", "voter shifts {country}",
            "parliamentary election analysis", "{year}"
        ]
    },
    "voting metrics": {
        "SEO-title":
        "{country} Voter metrics chart",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Interactive voting metrics chart displaying the {country} presidential election results, with percentage of registered voters who voted and percentage invalid votes across election years.",
        "SEO-description":
        "Explore detailed charts on {country}'s presidential election voter metrics results from 1969 to {year}, including voter turnout percentages and invalid vote statistics across election years. [...]",
        "SEO-keywords": [
            "{country} presidential election results",
            "{country} voter turnout", "{country} invalid vote statistics",
            "{country} election trends", "{country} voter participation",
            "{country} election data", "{country} electoral landscape",
            "African elections analysis", "{country} democracy trends",
            "{country} election charts",
            "{country} presidential voter metrics",
            "{country} election years 1969-{year}",
            "{country} voter turnout percentages",
            "{country} invalid votes by year",
            "{country} eligible voter trends", "{country} election research",
            "{country} political analysis", "{country} election observers",
            "{country} elections for students",
            "{country} elections for historians",
            "{country} elections for journalists",
            "{country} elections for civil society",
            "African voter turnout trends", "African invalid vote statistics",
            "{country} election visualizations",
            "{country} democracy analysis", "{country} democracy",
            "{country} election", "{country} election results",
            "{country} historical election results",
            "{country} parliament results", "{country} legislative control",
            "{country} presidential election voter metrics results",
            "percentage votes by political parties",
            "percentage of registered voters who voted",
            "percentage invalid votes", "election trends in {country}",
            "{country} political landscape", "{country} democracy",
            "voter shifts {country}", "political party performance {country}",
            "presidential election analysis", "When is {country} election?",
            "When will {country} elect president?",
            "Who won {country} election?", "Who won {country} president?",
            "Which party won in {country}?"
        ]
    },
    "bar": {
        "SEO-title":
        "{country} {year} total result bar chart",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Bar chart displaying the {year} {country} presidential election results, illustrating how each coalition party performed in terms of percentage of votes received.",
        "SEO-description":
        "Explore detailed charts on {country}'s presidential election results, with percentage votes broken down by political parties across election years. These visualizations provide essential insi[...]",
        "SEO-keywords": [
            "{country} democracy", "{country} election",
            "{country} presidential election results",
            "{country} election trends", "{country} percentage votes by party",
            "{country} political party performance",
            "{country} election analysis", "{country} party shifts",
            "{country} voter shifts",
            "{country} presidential vote percentages",
            "African elections analysis", "{country} democracy trends",
            "{country} presidential election charts",
            "{country} election years analysis", "{country} political trends",
            "{country} party vote breakdown", "{country} political analysis",
            "{country} election performance", "{country} voter trends",
            "{country} party performance trends",
            "{country} presidential voting data",
            "{country} election visualizations", "African democracy analysis",
            "{country} historical election results",
            "{country} electoral insights", "{country} election results",
            "percentage votes by political parties",
            "election trends in {country}", "{country} political landscape",
            "{country} democracy", "{country} election charts",
            "presidential election analysis", "vote manipulation",
            "When is {country} election?",
            "When will {country} elect president?", "nonpartisan",
            "Who won {country} election?", "Who won {country} president?",
            "Which party won {country}?", "{country} {year} election results",
            "rigging", "corruption", "{country} voter turnout",
            "{country} subnational results", "{country} parliament results",
            "{country} legislative control", "{country} election integrity",
            "{country} election audit", "{country} election reliability",
            "{country} election observation"
        ]
    },
    "map": {
        "SEO-title":
        "{country} {year} presidential election map",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Interactive map chart displaying the {year} {country} presidential election results, illustrating how each party and/or candidate performed by region based on the number of votes received acr[...]",
        "SEO-description":
        "Navigate through our interactive map visualizations of {country}'s presidential election data across regions and election years. These maps highlight key patterns, including election results,[...]",
        "SEO-keywords": [
            "{year}", "African election maps", "African elections",
            "African elections map analysis", "Election trends in {country}",
            "Interactive {country} election map",
            "{country} {year} election results",
            "{country} candidate vote counts", "{country} democracy",
            "{country} democracy visualizations", "{country} election",
            "{country} election audit", "{country} election corruption",
            "{country} election data by region", "{country} election insights",
            "{country} election integrity", "{country} election mapping",
            "{country} election observation", "{country} election reliability",
            "{country} election results", "{country} election trends by map",
            "{country} electoral geography", "{country} electoral maps",
            "{country} historical election results",
            "{country} legislative control", "{country} parliament results",
            "{country} political analysis by region",
            "{country} political maps", "{country} presidential election data",
            "{country} presidential election map",
            "{country} presidential election results",
            "{country} presidential election visualizations",
            "{country} regional democracy trends",
            "{country} regional election results",
            "{country} regional voting trends", "{country} ruling party map",
            "{country} subnational election results",
            "{country} subnational results", "{country} vote manipulation",
            "{country} voter turnout", "{country} voting patterns",
            "Percentage votes by political parties {country}",
            "Regional voting patterns {country}",
            "Shifting voter trends {country}",
            "When is {country}'s presidential election?",
            "When will {country} elect a president?",
            "Who won {country} president?", "Who won {country}'s election?",
            "Which party won in {country}?", "nonpartisan"
        ]
    },
    "election integrity": {
        "SEO-title":
        "{country} Election Integrity Chart",
        "sandbox":
        "allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation",
        "SEO-figcaption":
        "Election integrity chart displaying observer group estimates, official electoral body data, and discrepancies in vote counts, highlighting areas of potential irregularities or alignment betwe[...]",
        "SEO-description":
        "Explore {country}'s election integrity data, with observer group estimates and official electoral body estimates across election years. These data provide essential insights into {country}'s [...]",
        "SEO-keywords": [
            "{country} election integrity data",
            "observer group estimates {country}",
            "official electoral body estimates {country}",
            "election integrity trends", "parallel vote tabulation data",
            "discrepancies in election results",
            "election observers {country}",
            "election transparency in {country}", "pvt", "prvt",
            "political party performance {country}",
            "Would the discrepancy have changed who won the overall election results?",
            "Was the winning party the same?", "election observers",
            "{country} parliamentary election results",
            "number of seats by political parties",
            "{country} political landscape", "African elections", "{year}",
            "{country} democracy", "voter shifts {country}",
            "{country} election charts", "presidential election analysis",
            "When is {country} parliamentary election?",
            "When will {country} elect president?",
            "Who won {country} parliament seats?",
            "Which party won {country} election?", "{country} democracy",
            "{country} election", "{country} parliamentary results",
            "{country} historical election results",
            "{country} parliamentary results", "{country} voter turnout",
            "{country} subnational results", "{country} parliament results",
            "{country} legislative control", "{country} election integrity",
            "{country} election audit", "{country} election reliability",
            "rigging", "corruption", "vote manipulation", "nonpartisan",
            "{country} election observation"
        ]
    }
}

# Alias mapping for chart types found in a.json to the seo templates
charttype_aliases = {
    "key stats": "key stats",
    "democratic history": "democratic history",
    "one-candidates": "candidates",
    "two-candidates": "candidates",
    "three-candidates": "candidates",
    "four-candidates": "candidates",
    "candidates": "candidates",
    "parliament": "parliament",
    "senate parliament": "parliament",
    "national parliament": "parliament",
    "bar": "bar",
    "voting metrics": "voting metrics",
    "map": "map",
    "voter preference bar": "bar",
    "election integrity": "election integrity",
    "election representativeness": "election integrity",
}

def parse_seo_keywords(seo_keywords):
    if seo_keywords and isinstance(seo_keywords, str):
        return [kw.strip() for kw in seo_keywords.split(",") if kw.strip()]
    return seo_keywords  # already a list or None

def fill_seo_fields(section_data, charttype, country, year):
    charttype_key = charttype_aliases.get(charttype.lower(), charttype.lower())
    template = seo_templates.get(charttype_key)
    if not template:
        return section_data

    replacements = {
        "country": country,
        "year": year,
        "year_plus_5": str(int(year) + 5) if year and year.isdigit() else "",
        "year_plus_10": str(int(year) + 10) if year and year.isdigit() else "",
        "prev_year": str(int(year) - 5) if year and year.isdigit() else "",
        "next_year": str(int(year) + 5) if year and year.isdigit() else "",
    }
    for key, value in template.items():
        seo_field = key
        if not section_data.get(seo_field):
            if isinstance(value, str):
                section_data[seo_field] = value.format(**replacements)
            elif isinstance(value, list):
                section_data[seo_field] = [
                    v.format(**replacements) for v in value
                ]
    return section_data

def extract_country_data(base) -> Dict[str, Any]:
    pages = base.table("Pages").all()
    tabs = base.table("Tabs").all()
    subtabs = base.table("Subtabs").all()
    sections = base.table("Sections").all()

    tab_lookup = {t["id"]: t for t in tabs}
    subtab_lookup = {s["id"]: s for s in subtabs}
    section_lookup = {s["id"]: s for s in sections}

    result = {}

    for page in pages:
        fields = page["fields"]
        if not fields.get("PublishStatus"):
            continue

        page_id = fields.get("PageID")
        tab_ids = fields.get("TabID", [])
        country_data = {"page_fields": fields.copy(), "tabs": []}

        for tab_id in tab_ids:
            tab = tab_lookup.get(tab_id)
            if not tab or not tab["fields"].get("PublishStatus"):
                continue

            tab_fields = tab["fields"]
            subtab_ids = tab_fields.get("SubtabID", [])
            tab_data = {"tab_fields": tab_fields.copy(), "subtabs": []}

            # Build all subtabs first
            built_subtabs = []
            for subtab_id in subtab_ids:
                subtab = subtab_lookup.get(subtab_id)
                if not subtab or not subtab["fields"].get("SubtabShow"):
                    continue

                subtab_fields = subtab["fields"]
                section_ids = subtab_fields.get("SectionID", [])
                subtab_data = {
                    "subtab_fields": subtab_fields.copy(),
                    "sections": []
                }

                for section_id in section_ids:
                    section = section_lookup.get(section_id)
                    if not section or section["fields"].get(
                            "ShowSection") != "Yes":
                        continue

                    section_data = section["fields"].copy()
                    section_data["SEO-keywords"] = parse_seo_keywords(
                        section_data.get("SEO-keywords"))
                    section_data["ChartTitle"] = section_data.get(
                        "ChartTitle", "")
                    charttype = section_data.get("Charttype", "").lower()
                    country = fields.get("Country", "")
                    year = section_data.get("Year", "")
                    section_data = fill_seo_fields(section_data, charttype,
                                                   country, year)
                    subtab_data["sections"].append(section_data)

                built_subtabs.append(subtab_data)

            # Merge candidate charts into Presidential Election Results subtab
            # Identify the result and candidates subtabs
            result_subtab = None
            candidates_subtab = None
            for subtab in built_subtabs:
                title = subtab["subtab_fields"].get("SubtabTitle", "").lower()
                if "presidential election results" in title:
                    result_subtab = subtab
                elif "presidential candidates" in title:
                    candidates_subtab = subtab

            if result_subtab and candidates_subtab:
                # Group candidate sections by year
                from collections import defaultdict
                candidate_sections_by_year = defaultdict(list)
                sections_without_year = []  # For sections that should appear for all years
                
                for section in candidates_subtab["sections"]:
                    year = section.get("Year")
                    if year and year.strip():  # Only group if year exists and is not empty
                        candidate_sections_by_year[year].append(section)
                    else:
                        sections_without_year.append(section)  # These appear for all years

                # Group result sections by year
                results_sections_by_year = defaultdict(list)
                results_without_year = []  # For sections that should appear for all years
                
                for section in result_subtab["sections"]:
                    year = section.get("Year")
                    if year and year.strip():  # Only group if year exists and is not empty
                        results_sections_by_year[year].append(section)
                    else:
                        results_without_year.append(section)  # These appear for all years

                # Get all unique years from sections that have years
                all_years = set(candidate_sections_by_year) | set(results_sections_by_year)
                merged_sections = []
                
                # First, add sections without years (these appear for all years like voter metrics)
                merged_sections.extend(sections_without_year)
                merged_sections.extend(results_without_year)
                
                # Then add year-specific sections
                for year in sorted(all_years, reverse=True):
                    # Add candidate sections first (if any)
                    merged_sections.extend(candidate_sections_by_year.get(year, []))
                    # Then add results sections (bar, map, etc.)
                    merged_sections.extend(results_sections_by_year.get(year, []))
                
                result_subtab["sections"] = merged_sections

                # Optionally clear out the candidates subtab
                candidates_subtab["sections"] = []

            tab_data["subtabs"] = built_subtabs
            country_data["tabs"].append(tab_data)

        result[page_id] = country_data

    return result

def extract_democracy_data(base) -> Dict[str, Any]:
    pages = base.table("Democracy-pages").all()
    tabs = base.table("Democracy-tabs").all()
    subtabs = base.table("Democracy-subtabs").all()
    sections = base.table("Democracy-sections").all()

    # Create lookups using Airtable record IDs
    tab_lookup = {t["id"]: t for t in tabs}
    subtab_lookup = {s["id"]: s for s in subtabs}
    section_lookup = {s["id"]: s for s in sections}

    result = {}

    for page in pages:
        fields = page["fields"]
        page_id = fields.get("Democracy-pageID")
        if not page_id:
            continue

        tab_ids = fields.get("Democracy-tabID", [])
        page_data = {"page_fields": fields.copy(), "tabs": []}

        for tab_id in tab_ids:
            tab = tab_lookup.get(tab_id)
            if not tab:
                continue

            tab_fields = tab["fields"]
            tab_data = {"tab_fields": tab_fields.copy(), "subtabs": []}

            # Get subtabs for this tab using Airtable record IDs
            tab_subtab_ids = tab_fields.get("Democracy-subtabID", [])

            for subtab_id in tab_subtab_ids:
                subtab = subtab_lookup.get(subtab_id)
                if not subtab:
                    continue

                subtab_fields = subtab["fields"]
                subtab_data = {
                    "subtab_fields": subtab_fields.copy(),
                    "sections": []
                }

                # Get sections for this subtab using Airtable record IDs
                subtab_section_ids = subtab_fields.get("Democracy-sectionID",
                                                       [])

                for section_id in subtab_section_ids:
                    section = section_lookup.get(section_id)
                    if not section:
                        continue

                    section_fields = section["fields"].copy()
                    section_fields["SEO-keywords"] = parse_seo_keywords(
                        section_fields.get("SEO-keywords"))
                    # Ensure Charttitle field is captured
                    section_fields["Charttitle"] = section_fields.get(
                        "Charttitle", "")
                    subtab_data["sections"].append(section_fields)

                tab_data["subtabs"].append(subtab_data)

            page_data["tabs"].append(tab_data)

        result[page_id] = page_data

    return result

def load_data_from_airtable() -> None:
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")

    if not all([api_key, base_id]):
        raise ValueError("Missing API credentials")

    api = Api(api_key)
    base = api.base(base_id)

    print("Fetching Airtable data")

    countries = extract_country_data(base)
    democracy = extract_democracy_data(base)

    combined = {"countries": countries, "democracy": democracy}
    os.makedirs("siteV2/data", exist_ok=True)
    with open("siteV2/data/africa_pages.json", "w") as f:
        json.dump(combined, f, indent=2)

    print("Data written to africa_pages.json")
    return combined

if __name__ == "__main__":
    load_data_from_airtable()