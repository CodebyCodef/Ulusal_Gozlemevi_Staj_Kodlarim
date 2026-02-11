

using System.ComponentModel.DataAnnotations;

namespace denemeAPI.Models
{
    public class TaskItem
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Title alaný belirtmek zorunludur!!!")]
        [MinLength(3,ErrorMessage = "Title en az 3 karakterden oluþturulmalýdýr.")]

        public string? Title { get; set; } = string.Empty;
        public bool IsCompleted { get; set; }

    }
}