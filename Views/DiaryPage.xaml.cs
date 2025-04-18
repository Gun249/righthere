using Microsoft.Maui.Controls;
using System;
using System.Threading.Tasks;
using Righthere_Demo.Services;

namespace Righthere_Demo.Views
{
    public partial class DiaryPage : ContentPage
    {
        private readonly DiaryService _diaryService;

        public DiaryPage()
        {
            InitializeComponent();
            _diaryService = new DiaryService("");
        }
        protected override void OnAppearing()
        {
            base.OnAppearing();
            Console.WriteLine("📍 DiaryPage Appeared");
        }

        private async void OnAnalyzeClicked(object sender, EventArgs e)
        {
            string content = DiaryEntry.Text;

            // ✅ แสดง Loading และปิดปุ่ม
            AnalyzeButton.IsEnabled = false;
            AnalyzeButton.Text = "Loading...";
            LoadingIndicator.IsVisible = true;
            LoadingIndicator.IsRunning = true;

            // ✅ ใช้ instance API
            Services.API api = new Services.API();
            await api.SendData(content);

            // ✅ ดึงค่าจาก API
            string mood = api.GetMood();
            string suggestion = api.GetSuggestion();
            string keyword = api.GetKeywords();
            string emotion = api.GetEmotionalReflection();

            Console.WriteLine("Sending Mood to SummaryPage: " + mood);

            // ✅ ซ่อน Loading และคืนค่าปุ่ม
            AnalyzeButton.IsEnabled = true;
            AnalyzeButton.Text = "Next ➤";
            LoadingIndicator.IsVisible = false;
            LoadingIndicator.IsRunning = false;

            // ✅ เปิดหน้า SummaryPage พร้อมส่งค่าที่ได้จาก API
            await Navigation.PushAsync(new SummaryPage(mood, suggestion, keyword, emotion));
        }
    }
}
