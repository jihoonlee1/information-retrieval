import database


okay = """Analyzing the provided images for business activities within the specified scope and exclusion criteria, here are the findings:

IMAGE21:
- Installation, maintenance and repair of energy efficiency equipment (Code 7.3): The turnover amount for this activity is €10,874,063, representing 0.10% of total turnover. This activity aligns with the scope of installing energy-efficient equipment for buildings.

IMAGE22:
No additional relevant activities were found in comparison to IMAGE21.

IMAGE23:
No additional relevant activities were found in comparison to IMAGE21.

Based on the scope that focuses on activities related to the installation, maintenance, and repair of energy-efficient equipment for buildings (insulation, windows, doors, HVAC systems, boilers, pumps, LED systems, and low-flow water fittings) and excluding larger-scale building renovations and specialized services such as assessments, the relevant activity from these images is as follows:

[IMAGE21; Installation, maintenance and repair of energy efficiency equipment; 10874063]"""
with database.connect() as con:
	cur = con.cursor()
	cur.execute("INSERT INTO pdf_key_activity_temp VALUES(?,?,?,?)", (0, "revenue", "Installation, Maintenance and Repair of Energy Efficiency Equipment​", okay))
	con.commit()