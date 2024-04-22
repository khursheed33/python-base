from langchain.output_parsers import StructuredOutputParser, ResponseSchema


class LLMResponseSchemas:
    # Rephrase Response
    rephrase_response_schemas = [
        ResponseSchema(
            name='response', description='Response should be a markdown. If there are sub points or list then return them in a markdown. Use bullet points and other.'),
    ]
    rephrase_output_parser = StructuredOutputParser.from_response_schemas(
        rephrase_response_schemas)
    rephrase_format_instructions = rephrase_output_parser.get_format_instructions()
