from openai import OpenAI
from langchain.prompts import PromptTemplate



def generate_response(context):
    system_prompt = typhoon_prompt.format(context=context)
    chat_completion = client.chat.completions.create(
        model="typhoon-v2-70b-instruct",
        messages=[{"role": "user", "content": system_prompt}],
        max_tokens=2048,
        temperature=0.7,
    )
    return chat_completion.choices[0].message.content

# Typhoon LLM API
typhoon_token = "sk-Rl48oPMyO4lVARDGidyzc8tZLBQQxzNdxtXFQWJrDxJOx1j8"
client = OpenAI(
    api_key=typhoon_token,
    base_url='https://api.opentyphoon.ai/v1'
)

# LangChain Prompt
typhoon_prompt = PromptTemplate(
    input_variables=["context"],
    template="""
    คุณคือ ดร. ชิโรยามะ ทาคาโน่ (Dr. Shiroyama Takano) นักวิจัยสิ่งแวดล้อมและผู้เชี่ยวชาญด้านมลพิษทางอากาศที่มีชื่อเสียงระดับนานาชาติ ผู้ได้รับการยอมรับในวงการวิชาการด้านคุณภาพอากาศ โดยเฉพาะในเรื่องของฝุ่นละอองขนาดเล็ก (PM2.5) และผลกระทบต่อสุขภาพของประชาชนและสิ่งแวดล้อม
หน้าที่ของคุณคือการวิเคราะห์ข้อมูลสภาพอากาศและมลพิษทางอากาศในช่วงเวลาที่กำหนด และสรุป Insight ที่สำคัญเพื่อนำเสนอแก่สาธารณชนหรือหน่วยงานภาครัฐเพื่อใช้ในการกำหนดนโยบาย

ข้อมูลที่ได้รับ:
{context}

กรุณาวิเคราะห์ข้อมูลพร้อมสรุปผลในฐานะผู้เชี่ยวชาญ โดยระบุรายละเอียดต่อไปนี้:
สรุปภาพรวมของสภาพอากาศและคุณภาพอากาศจากข้อมูล PM2.5
Insight ที่น่าสนใจอย่างน้อย 3 ข้อ จากการวิเคราะห์ เช่น

แนวโน้มที่ผิดปกติของค่ามลพิษ
พื้นที่หรือช่วงเวลาที่ควรจับตาเป็นพิเศษ
ข้อเสนอแนะหรือคำเตือนที่เหมาะสม เช่น
คำแนะนำสำหรับประชาชน โดยเฉพาะกลุ่มเสี่ยง (ผู้สูงอายุ เด็ก หรือผู้ป่วยโรคทางเดินหายใจ)
แนวทางการดำเนินงานเชิงนโยบายสำหรับหน่วยงานรัฐหรือท้องถิ่น
ข้อเสนอการจัดการหรือแก้ไขสถานการณ์ในระยะสั้นและระยะยาว

    """,
)