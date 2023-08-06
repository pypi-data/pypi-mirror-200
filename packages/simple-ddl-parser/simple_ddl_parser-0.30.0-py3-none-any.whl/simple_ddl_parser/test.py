from simple_ddl_parser import DDLParser
ddl = """
    CREATE TABLE data.test(
        field_a INT OPTIONS(description='some description')
    )
    PARTITION BY RANGE_BUCKET(field_a, GENERATE_ARRAY(10, 1000, 1));
    """

result = DDLParser(ddl).run()

import pprint
pprint.pprint(result)
