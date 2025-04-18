using System;
using System.Text.Json.Serialization;
using BCrypt.Net;

namespace Righthere_Demo.Models;

public class User
{
    [JsonPropertyName("userid")]
    public int UserId { get; set; }

    [JsonPropertyName("username")]
    public string Username { get; set; }

    [JsonPropertyName("email")]
    public string Email { get; set; }

    [JsonPropertyName("password")]
    public string Password { get; set; }

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }
}

