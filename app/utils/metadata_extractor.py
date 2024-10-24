import os
import json
from typing import List, Dict, Any
from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
import tiktoken
from app.llm.langchain_openai_manager import OpenAIManager

class DocumentMetadata(BaseModel):
    entities: List[Dict[str, str]] = Field(description="List of named entities and their types")
    keywords: List[str] = Field(description="List of important keywords from the text")
    sentiment: float = Field(description="Sentiment score from -1 (negative) to 1 (positive)")
    main_topics: List[str] = Field(description="Main topics discussed in the text")
    summary: str = Field(description="Brief summary of the text content")
    page_numbers: List[int] = Field(description="Page numbers this chunk corresponds to")

class DocumentProcessor:
    def __init__(self, output_dir: str = "output"):
        self.openai_manager = OpenAIManager()
        self.output_dir = output_dir
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        
        # Initialize processing components
        self.setup_components()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def setup_components(self):
        """Initialize processing components"""
        self.parser = PydanticOutputParser(pydantic_object=DocumentMetadata)
        
        # Create prompt template for extraction
        template = """You are an expert at analyzing text and extracting meaningful information.
        Extract the following information from the provided text:
        1. Named entities and their types
        2. Important keywords
        3. Overall sentiment (score from -1 to 1)
        4. Main topics discussed
        5. Brief summary
        
        {format_instructions}
        
        Text to analyze: {text}
        """
        
        self.prompt_template = PromptTemplate(
            template=template,
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string"""
        return len(self.encoding.encode(text))

    def load_document(self, file_path: str) -> List[str]:
        """Load document and return pages as a list of strings"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")
        
        # Load all pages
        pages = loader.load()
        return pages

    def save_results(self, results: List[Dict], file_path: str):
        """Save results to a JSON file"""
        filename = os.path.join(self.output_dir, f"{os.path.basename(file_path)}_results.json")
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

    def process_document(self, file_path: str) -> str:
        """Process a document and extract metadata"""
        pages = self.load_document(file_path)
        all_results = []

        # Combine text from all pages into a single string for processing
        combined_text = "\n\n".join(page.page_content for page in pages)

        # Split the combined text into chunks of max 40,000 characters
        text_splitter = CharacterTextSplitter(
            chunk_size=40000,  # Maximum chunk size
            chunk_overlap=1000  # Overlap between chunks
        )
        chunks = text_splitter.split_text(combined_text)
        
        for chunk in chunks:
            # Check token count
            if self.count_tokens(chunk) > 12000:  # Limit for processing
                print(f"Warning: Chunk too large ({self.count_tokens(chunk)} tokens), skipping")
                continue
            
            try:
                # Process the chunk using OpenAIManager
                result = self.openai_manager.run_llm_chain(
                    prompt_template=self.prompt_template,
                    output_parser=self.parser,
                    input_values={"text": chunk}
                )
                
                # Add corresponding page numbers
                # Assuming chunk starts from the first page, we need to adjust based on the actual range of pages
                page_numbers = list(range(1, len(pages) + 1))
                result_dict = result.dict() if hasattr(result, 'dict') else result
                result_dict['page_numbers'] = page_numbers  # Adjust if needed
                all_results.append(result_dict)

            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
                continue
        
        # Save all results to a single JSON file
        self.save_results(all_results, file_path)
        return os.path.join(self.output_dir, f"{os.path.basename(file_path)}_results.json")
