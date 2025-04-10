using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace Righthere_Demo.Services;

public class SupabaseService
{
    private readonly HttpClient _httpClient;
    private readonly string _supabaseUrl;
    private readonly string _apiKey;

    public SupabaseService()
    {
        _supabaseUrl = Environment.GetEnvironmentVariable("SUPABASE_URL") ?? throw new Exception("SUPABASE_URL not set");
        _apiKey = Environment.GetEnvironmentVariable("SUPABASE_KEY") ?? throw new Exception("SUPABASE_KEY not set");

        _httpClient = new HttpClient();
        _httpClient.BaseAddress = new Uri(_supabaseUrl);
        _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _apiKey);
        _httpClient.DefaultRequestHeaders.Add("apikey", _apiKey);
        _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
    }

    public async Task<string> InsertDiaryEntry(string content, string mood)
    {
        var json = $"[{{\"content\":\"{content}\",\"mood\":\"{mood}\"}}]";
        var contentData = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await _httpClient.PostAsync("/rest/v1/diary", contentData);

        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadAsStringAsync();
        }

        return $"Error: {response.StatusCode} - {await response.Content.ReadAsStringAsync()}";
    }
}
