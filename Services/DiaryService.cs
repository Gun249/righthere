using System;

namespace Righthere_Demo.Services;

public class DiaryService
{
    private string _content;

    public DiaryService(string content)
    {
        _content = content;
    }

    public string GetContent()
    {
        return _content;
    }

    public void SetContent(string content)
    {
        _content = content;
    }

    // สามารถเพิ่ม method สำหรับประมวลผล, บันทึก, วิเคราะห์ ได้ในอนาคต
    public string AnalyzeMood()
    {
        // สมมุติว่าเราจะวิเคราะห์ความรู้สึกจากข้อความ
        if (string.IsNullOrWhiteSpace(_content))
            return "Neutral";

        if (_content.Contains("happy") || _content.Contains("joy"))
            return "Happy";
        else if (_content.Contains("sad") || _content.Contains("depressed"))
            return "Sad";
        else
            return "Neutral";
    }

}
