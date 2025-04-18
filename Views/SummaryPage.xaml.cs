using Microsoft.Maui.Controls;
using System;

namespace Righthere_Demo.Views
{
    public partial class SummaryPage : ContentPage
    {
        private string mood;
        private string Sugges;
        private string keyword;
        private string Emotion;

        public SummaryPage(string mood, string Suggestion, string Keyword, string Emotion)
        {
            InitializeComponent();

            this.mood = mood;
            this.Sugges = Suggestion;
            this.keyword = Keyword;
            this.Emotion = Emotion;

            // ✅ ใช้ OnAppearing() เพื่ออัปเดต UI
        }

        // ✅ ใช้ OnAppearing() เพื่ออัปเดต UI เมื่อหน้าพร้อม
        protected override void OnAppearing()
        {
            base.OnAppearing();

            if (Moodtex != null)
                Moodtex.Text = this.mood;  // ✅ อัปเดตค่า Label
            Advicetext.Text = this.Sugges;
            Keywordtext.Text = this.keyword;
            Emotiontext.Text = this.Emotion;
        }
        private void GoMainPage(object sender, EventArgs e)
        {
            Application.Current.MainPage = new NavigationPage(new MainPage());

        }


    }
}
