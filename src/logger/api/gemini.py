"""Gemini API integration for content analysis."""
import json
from typing import Optional, Dict, Any
from pathlib import Path

import google.generativeai as genai
from PIL import Image


class GeminiAnalyzer:
    """Analyzer using Google's Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """Initialize the Gemini analyzer.
        
        Args:
            api_key: Google API key for Gemini
            model_name: Model name to use (default: gemini-1.5-flash)
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def analyze_content(
        self,
        text: Optional[str] = None,
        image_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze text and/or image content.
        
        Args:
            text: Text content to analyze
            image_path: Path to image file to analyze
            
        Returns:
            Dictionary containing:
                - summary: Brief summary of the activity (50-100 chars)
                - category: Activity category
                - tags: List of relevant tags
                - duration_estimate: Estimated duration in minutes
        """
        if not text and not image_path:
            raise ValueError("Either text or image_path must be provided")
        
        # Prepare the prompt
        prompt = self._create_analysis_prompt()
        
        # Prepare content for the model
        content_parts = [prompt]
        
        if text:
            content_parts.append(f"\n\n文字内容：\n{text}")
        
        if image_path and Path(image_path).exists():
            try:
                image = Image.open(image_path)
                content_parts.append(image)
            except Exception as e:
                print(f"Warning: Failed to load image: {e}")
        
        # Generate response
        try:
            response = self.model.generate_content(content_parts)
            result = self._parse_response(response.text)
            return result
        except Exception as e:
            # Fallback response if API fails
            return {
                "summary": text[:100] if text else "图片内容",
                "category": "其他",
                "tags": [],
                "duration_estimate": 5,
                "error": str(e)
            }
    
    def _create_analysis_prompt(self) -> str:
        """Create the analysis prompt for Gemini."""
        return """你是一个智能生活日志助手。请分析用户提供的内容（文字和/或图片），并返回一个JSON格式的分析结果。

请严格按照以下JSON格式返回（不要包含markdown代码块标记，只返回纯JSON）：
{
  "summary": "简洁的活动总结，50-100字，描述用户在做什么",
  "category": "活动类型，必须是以下之一：工作、学习、娱乐、运动、社交、生活、其他",
  "tags": ["标签1", "标签2", "标签3"],
  "duration_estimate": 估计耗时的分钟数（整数）
}

分类说明：
- 工作：编程、开会、处理邮件、项目相关等
- 学习：阅读、上课、研究、学习新技能等
- 娱乐：看视频、玩游戏、听音乐、浏览社交媒体等
- 运动：健身、跑步、瑜伽、球类运动等
- 社交：聊天、聚会、社交活动等
- 生活：购物、做饭、打扫、日常琐事等
- 其他：无法明确分类的活动

请根据内容智能估计该活动可能花费的时间（以分钟为单位）。
标签应该提取3-5个最相关的关键词。"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the Gemini response.
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed dictionary with analysis results
        """
        try:
            # Remove markdown code block markers if present
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            # Parse JSON
            result = json.loads(cleaned_text)
            
            # Validate required fields
            required_fields = ["summary", "category", "tags", "duration_estimate"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate category
            valid_categories = ["工作", "学习", "娱乐", "运动", "社交", "生活", "其他"]
            if result["category"] not in valid_categories:
                result["category"] = "其他"
            
            # Ensure tags is a list
            if not isinstance(result["tags"], list):
                result["tags"] = []
            
            # Ensure duration_estimate is an integer
            result["duration_estimate"] = int(result["duration_estimate"])
            
            return result
        
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback if parsing fails
            return {
                "summary": response_text[:100] if len(response_text) < 500 else "内容分析",
                "category": "其他",
                "tags": [],
                "duration_estimate": 5,
                "parse_error": str(e)
            }


