using System;
using System.Collections.Generic;

namespace Firamir.GeneratedDomain
{
    // Сгенерировано по диаграмме классов (PlantUML) для использования как доменная модель.
    public class User
    {
        public int Id { get; set; }
        public string Login { get; set; }
        public string Password { get; set; }
        public int RoleId { get; set; }
        public Role Role { get; set; }
    }

    public class Role
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public ICollection<User> Users { get; set; } = new List<User>();
    }

    public class PatientCard
    {
        public int Id { get; set; }
        public string ChildFullName { get; set; }
        public DateTime BirthDate { get; set; }
        public DateTime AdmissionDate { get; set; }
        public ICollection<PatientVisit> Visits { get; set; } = new List<PatientVisit>();
    }

    public class PatientVisit
    {
        public int Id { get; set; }
        public int PatientCardId { get; set; }
        public DateTime VisitDate { get; set; }
        public string SpecialistName { get; set; }
        public string Conclusion { get; set; }
        public PatientCard PatientCard { get; set; }
    }
}
