using System.ComponentModel.DataAnnotations;


namespace APIforUsers.UserModel
{
    public class UserInfo
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "E-mail alaný boþ býrakýlamaz.")]
        [EmailAddress(ErrorMessage = "Geçerli bir e-mail adresi giriniz.")]

        public string Email { get; set; } = string.Empty;

        [Required(ErrorMessage = "Þifre alaný boþ býrakýlamaz.")]
        public string Password { get; set; } = string.Empty;



    }
}