<script>
    document.addEventListener('DOMContentLoaded', function () {
        // Fungsi untuk memuat data dari CSV
        function loadDataFromCSV() {
            d3.csv('C:\\Users\\Putra Jaya\\Documents\\SEMESTER 6\\Data Analytics Visualization\\Website_Dasbhoard\\Data_Gabungan.csv')
                .then(function(data) {
                    // Lakukan sesuatu dengan data yang dimuat
                    console.log(data); // Cek konsol untuk memastikan data berhasil dimuat
                    // Contoh: Update data di chart atau tampilkan data di elemen lain
                    // Misalnya, Anda bisa mengupdate bar chart atau data keseluruhan berdasarkan data CSV yang dimuat
                })
                .catch(function(error) {
                    console.error('Error loading the CSV file:', error);
                });
        }

        // Panggil fungsi untuk memuat data saat DOM selesai dimuat
        loadDataFromCSV();
    });
</script>