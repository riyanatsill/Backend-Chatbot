-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2025 at 10:56 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chatbot_pmb`
--

-- --------------------------------------------------------

--
-- Table structure for table `faq_final`
--

CREATE TABLE `faq_final` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `category` varchar(50) DEFAULT 'Umum',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faq_final`
--

INSERT INTO `faq_final` (`id`, `question`, `answer`, `category`, `created_at`, `updated_at`) VALUES
(1, 'Apa itu PMB?', 'PMB adalah proses penerimaan mahasiswa baru di Politeknik Negeri Jakarta untuk berbagai program studi yang tersedia.', 'Umum', '2025-05-14 06:53:08', '2025-05-14 06:53:08'),
(2, 'Kapan jadwal pendaftaran SNBT?', 'Pendaftaran SNBT di PNJ dimulai dari 11 sampai 27 Maret 2025.', 'Jadwal', '2025-05-14 06:56:21', '2025-05-16 08:11:46');

-- --------------------------------------------------------

--
-- Table structure for table `faq_suggestions`
--

CREATE TABLE `faq_suggestions` (
  `id` int(11) NOT NULL,
  `main_question` text NOT NULL,
  `answer` text DEFAULT NULL,
  `status` enum('pending','accepted','ignored') DEFAULT 'pending',
  `category` varchar(50) DEFAULT 'Umum'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faq_suggestions`
--

INSERT INTO `faq_suggestions` (`id`, `main_question`, `answer`, `status`, `category`) VALUES
(14, 'Berapa biaya pendaftaran Pascasarjana?', NULL, 'pending', 'Biaya');

-- --------------------------------------------------------

--
-- Table structure for table `faq_suggestion_variants`
--

CREATE TABLE `faq_suggestion_variants` (
  `id` int(11) NOT NULL,
  `suggestion_id` int(11) NOT NULL,
  `question` text NOT NULL,
  `similarity_score` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faq_suggestion_variants`
--

INSERT INTO `faq_suggestion_variants` (`id`, `suggestion_id`, `question`, `similarity_score`) VALUES
(28, 14, 'Berapa biaya pendaftaran Pascasarjana?', 1),
(29, 14, 'biaya pendaftaran pascasarjana berapa?', 1);

-- --------------------------------------------------------

--
-- Table structure for table `qa_data`
--

CREATE TABLE `qa_data` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qa_data`
--

INSERT INTO `qa_data` (`id`, `question`, `answer`, `filename`, `created_by`, `created_at`) VALUES
(147, 'Apa itu PMB di Politeknik Negeri Jakarta?', 'PMB adalah proses penerimaan mahasiswa baru di Politeknik Negeri Jakarta untuk berbagai program studi yang tersedia.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(148, 'Apa saja jalur penerimaan mahasiswa baru di PNJ?', 'Jalur penerimaan mahasiswa baru di PNJ meliputi SNBP, SNBT, jalur mandiri, Mandiri Prestasi, Kelas Kerjasama, Program RPL (Rekognisi Pembelajaran Lampau), Program Pacasarjana, D1 Teknik Komputer dan Jaringan, Program D3 Manajemen Pemasaran Untuk Warga Negara Berkebutuhan Khusus (WNBK) Jurusan Akutansi, International Student Admission dan Program Studi di luar kampus utama (PSDKU)', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(149, 'Apakah ada beasiswa bagi mahasiswa baru di PNJ?', 'Ya, PNJ menyediakan berbagai beasiswa seperti Bidikmisi, KIP Kuliah, dan beasiswa prestasi.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(150, 'Bagaimana alur pendaftaran online di PNJ?', 'Alur pendaftaran online meliputi pembuatan akun, pengisian formulir, unggah dokumen, dan pembayaran biaya pendaftaran. Untuk lebih jelasnya calon mahasiswa bisa mengakses laman resmi penerimaan mahasiswa di ‘https://penerimaan.pnj.ac.id/‘', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(151, 'Apa itu SNBP?', 'SNBP merupakan Seleksi Nasional Berdasarkan Prestasi yang menggunakan nilai rapor tanpa ujian tulis.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(152, 'Apa itu SNBT?', 'SNBT adalah Seleksi Nasional Berdasarkan Tes yang menggunakan hasil ujian tulis sebagai dasar seleksi.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(153, 'Apa itu Ujian mandiri?', 'Jalur Uijan mandiri adalah kesempatan terakhir dari rangkaian penerimaan mahasiswa baru Politeknik Negeri Jakarta untuk Tahun Akademik 2024/2025. Seleksi berdasarkan kemampuan akademis mengunakan test online, bila lulus peserta hanya dapat memilih Uang Kuliah Tunggal (UKT) Kelompok VI – VIII dan Iuran Pengembangan Institusi (IPI) sebesar Rp 12.5 juta (Program Studi Bidang Rekayasa) dan Rp. 10 juta (Program Studi Bidang Tata Niaga).', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(154, 'Apa itu Jalur Mandiri Prestasi?', 'Ini jalur yang memberikan kesempatan bagi siswa lulusan SMA/SMK/MA/sederajat yang memiliki prestasi akademik dan non-akademik yang bertujuan untuk memperoleh calon mahasiswa yang memiliki prestasi unggul. Seleksi berdasarkan nilai akademik atau prestasi akademik lainnya dengan menggunakan rapor semester 1 sampai dengan semester 5 dan non akademik dengan menggunakan sertifikat kejuaraan. Para pendaftar harus memperhatikan jadwal dan persyaratan yang telah ditentukan oleh Politeknik Negeri Jakarta.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(155, 'Apa itu program Kelas Kerjasama di PNJ?', 'Kelas Kerjasama di PNJ adalah program pendidikan yang diselenggarakan melalui kemitraan antara PNJ dan berbagai lembaga, institusi, atau perusahaan, baik dari dalam maupun luar negeri. Program ini memberikan kesempatan bagi lulusan SMA/SMK untuk melanjutkan pendidikan ke jenjang Diploma dan Sarjana Terapan dengan kurikulum yang dirancang khusus sesuai kebutuhan industri dan perkembangan teknologi. Pendaftaran untuk program Kelas Kerjasama biasanya dibuka pada periode tertentu setiap tahunnya. Informasi lebih lanjut mengenai pendaftaran dan persyaratan dapat diakses melalui situs resmi PNJ atau akun media sosial resmi.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(156, 'Apa itu program RPL?', 'Penerimaan Mahasiswa Program Rekognisi Pembelajaran Lampau (RPL) merupakan Program lanjutan Dari D3 ke S1 Terapan. Pengertian dari RPL itu sendiri adalah pengakuan terhadap Capaian Pembelajaran (CP) yang diperoleh seseorang dari pendidikan formal atau non formal atau informal, dan/atau pengalaman kerja pada jenjang pendidikan tinggi. Dalam program ini mata kuliah yang akan di RPL-kan adalah mata kuliah program Diploma 3 (D3) yang telah diampu calon mahasiswa sehingga dapat melanjutkan sampai jenjang S1 terapan pada program ini. Sementara ini, Program Studi yang sudah mendapatkan mandat penyelenggaraan dan siap melaksanakan program RPL adalah D4 Teknologi Rekayasa Konversi Energi (RESD), D4 Teknik Perancangan Jalan dan Jembatan, D4 Teknologi Rekayasa Pemeliharaan Alat Berat, D4 Teknologi Rekayasa Manufaktur.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(157, 'Apa itu program Pascasarjana?', 'Pada saat ini, Program Pascasarjana Politeknik Negeri Jakarta mengelola dua Program Studi, yaitu Program Studi Magister Terapan Teknik Elektro (S2 Teknik Elektro/MTTE) dan Magister Terapan Rekayasa Teknologi Manufaktur (S2 Manufaktur/MTRTM). Program Pascasarjana Politeknik Negeri Jakarta membuka peneriman mahasiswa baru Program Magister, pada program studi: Magister Terapan Teknik Elektro (MTTE) dan Magister Terapan Rekayasa Teknologi Manufaktur (MTRTM). Kedua program tersebut adalah Strata-2 (S2) dengan gelar Magister Terapan Teknik.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(158, 'Apa itu program Studi D1 Teknik Komputer dan Jaringan?', 'Program ini adalah program pendidikan vokasi jenjang Diploma 1 yang berfokus pada penguasaan keterampilan dasar di bidang teknologi komputer dan jaringan. Program ini dirancang untuk menghasilkan lulusan yang kompeten dalam instalasi, konfigurasi, dan pemeliharaan jaringan komputer, serta memiliki pemahaman dasar tentang keamanan jaringan dan pemrograman jaringan.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(159, 'Apa itu program Warga Negara Berkebutuhan Khusus (WNBK)?', 'Penerimaan Mahasiswa Baru (PMB) untuk Warga Negara Berkebutuhan Khusus (WNBK) di Politeknik Negeri Jakarta dibuka pada Program Studi D3 Manajemen Pemasaran Jurusan Akuntansi Politeknik Negeri Jakarta. Program tersebut terbuka bagi siswa different ability (difabel) lulusan SMA/SMK Inklusi maupun SMA/SMK-LB atau sederajat yang berminat mendalami ilmu Manajemen Pemasaran. Program Studi D3 Manajemen Pemasaran untuk WNBK di Jurusan Akuntansi Politeknik Negeri Jakarta bertujuan untuk menghasilkan lulusan yang mandiri dan memiliki kemampuan softskill serta hardskill dalam bidang pemasaran dan wirausaha. Sistem pembelajaran yang diterapkan pada program studi ini mencakup 30% teori dan 70% praktik. Saat ini Program Studi D3 Manajemen Pemasaran telah terakreditasi B.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(160, 'Apa itu Program Studi di Luar Kampus Utama (PSDKU)?', 'Program Studi di Luar Kampus Utama (PSDKU) merupakan program kerjasama Politeknik Negeri Jakarta dengan Pemerintah Daerah Kabupaten Demak dan Kota Pekalongan (Jawa Tengah) dalam penyelenggaraan pendidikan vokasi berbasis kompetensi keahlian sesuai dengan kebutuhan dunia usaha/ dunia industri. Diharapkan lulusan dari PSDKU PNJ dapat berperan dalam kemajuan industri di Kabupaten Demak, Kota Pekalongan (Jawa Tengah) dan sekitarnya. PNJ membuka beberapa program studi di lokasi PSDKU Demak dan PSDKU Kota Pekalongan. Di PSDKU Demak, terdapat D3 Teknik Mesin serta D4 Meeting, Incentive, Convention, and Exhibition (MICE). Sementara itu, di PSDKU Kota Pekalongan, program studi yang tersedia adalah D4 Manufaktur.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(161, 'Apakah ada jalur mandiri di PNJ?', 'Ya, PNJ memiliki jalur mandiri sebagai salah satu alternatif penerimaan mahasiswa baru.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(162, 'Bagaimana cara menghubungi panitia PMB PNJ?', 'Panitia PMB PNJ dapat dihubungi melalui kontak resmi di situs ‘https://penerimaan.pnj.ac.id/’ dengan, No. Telepon Humas: 021-7270036 & Chat Center: 0812-1110-0992. Surel: humas@pnj.ac.id, akademik@pnj.ac.id, transformasi.digital@pnj.ac.id.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(163, 'Program kelas Kerjasama PNJ ada apa saja ya?', 'Beberapa program Kelas Kerjasama yang ditawarkan oleh PNJ antara lain: \nPNJ - PT BADAK NGL\nPNJ - CCIT - FTUI\nPNJ - Jakarta Global University (JGU), \nPNJ - Holcim (PT. Solusi Bangun Indonesia), \nPNJ - Management and Science University (MSU),\nPNJ - PT. Formosa \nPNJ - Tongmyong University.', 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(164, 'Kapan Jadwal pendaftaran Seleksi Nasional Berdasarkan Prestasi (SNBP) di PNJ?', 'Jadwal pendaftaran SNBP dimulai pada tanggal 4 sampai 8 Februari 2025.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(165, 'Kapan jadwal pendaftaran Seleksi Nasional Berbasis Tes (SNBT) di PNJ?', 'Pendaftaran SNBT di PNJ dimulai dari 11 sampai 27 Maret 2025.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(166, 'Kapan jadwal pendaftaran Ujian Mandiri di PNJ?', 'Jadwal pendaftaran Ujian Mandiri dimulai tanggal 2 Mei sampai 13 Juni 2025.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(167, 'Kapan jadwal pendaftaran Ujian Mandiri Prestasi di PNJ?', 'Jadwal pendaftaran Mandiri Prestasi dimulai pada 15 Juni – 20 Juni 2024.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(168, 'Kapan jadwal pendaftaran Rekognisi Pembelajaran Lampau (RPL) di PNJ?', 'Jadwal pendaftaran RPL dimulai pada tanggal 28 April – 30 Juni 2025.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(169, 'Kapan jadwal pendaftaran Pascasarjana di PNJ?', 'Jadwal pendaftaran Pascasarjana gelombang 1adalah 3 Maret - 11 April 2025 dan Jadwal pendaftaran Pascasarjana gelombang 2 adalah 28 April - 30 Mei 2025.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(170, 'Kapan jadwal pendaftaran pendaftaran Program D3 Manajemen Pemasaran Untuk Warga Negara Berkebutuhan Khusus (WNBK) Jurusan Akutansi di PNJ?', 'Jadwal pendaftaran Program D3 Manajemen Pemasaran Untuk Warga Negara Berkebutuhan Khusus (WNBK) Jurusan Akutansi gelombang 1: 17 Februari 2025 – 26 Mei 2025 dan Untuk gelobang 2 adalah 28 Mei 2025 - 7 Juli 2025.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(171, 'Kapan jadwal pendaftaran Program International Student Admission Jurusan Akutansi di PNJ?', 'Jadwal pendaftaran Program Studi di luar kampus utama (PSDKU) dimulai 8 - 15 Juli 2024.', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47'),
(172, 'Kapan jadwal pendaftaran Program Studi di luar kampus utama (PSDKU) di PNJ?', 'Jadwal pendaftaran Program Studi di luar kampus utama (PSDKU) dimulai 8 - 15 Juli 2024', 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47');

-- --------------------------------------------------------

--
-- Table structure for table `uploaded_files`
--

CREATE TABLE `uploaded_files` (
  `id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `uploaded_by` varchar(100) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uploaded_files`
--

INSERT INTO `uploaded_files` (`id`, `filename`, `uploaded_by`, `uploaded_at`) VALUES
(8, 'Pertanyaan_Umum.docx', 'admin_zia', '2025-05-17 22:01:48'),
(9, 'Jadwal_2.docx', 'admin_zia', '2025-05-17 22:06:47');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','superadmin') NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'admin_master', 'superadmin@pnj.ac.id', '$2b$12$w33GM50zzirgL1TGsUhScufSSv1ATNAQ3TiWdogiUyg8K8OiZxmFy', 'superadmin', '2025-05-08 16:57:25'),
(2, 'admin_zia', 'zia@pnj.ac.id', '$2b$12$h4p/jRIQX6KxVmZ31d4Le.Fpj4MbZiL6hHizg9DROxw9VpkYS1QUW', 'admin', '2025-05-15 23:52:36');

-- --------------------------------------------------------

--
-- Table structure for table `user_questions`
--

CREATE TABLE `user_questions` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `finalized` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_questions`
--

INSERT INTO `user_questions` (`id`, `question`, `answer`, `created_at`, `finalized`) VALUES
(1, 'Apa itu PMB?', 'PMB adalah proses penerimaan mahasiswa baru di Politeknik Negeri Jakarta untuk berbagai program studi yang tersedia.', '2025-05-13 18:42:02', 1),
(2, 'PMB adalah?', 'PMB adalah proses penerimaan mahasiswa baru di Politeknik Negeri Jakarta untuk berbagai program studi yang tersedia.', '2025-05-13 18:48:23', 1),
(3, 'Apa itu PMB di PNJ?', 'PMB adalah proses penerimaan mahasiswa baru di Politeknik Negeri Jakarta untuk berbagai program studi yang tersedia.', '2025-05-13 18:48:43', 1),
(4, 'Kapan jadwal pendaftaran SNBT?', 'Pendaftaran SNBT di PNJ dimulai dari 11 sampai 27 Maret 2025.', '2025-05-14 06:46:48', 1),
(5, 'Jadwal Pendaftaran SNBT kapan?', 'Pendaftaran SNBT di PNJ dimulai dari 11 sampai 27 Maret 2025.', '2025-05-14 06:48:10', 1),
(6, 'apa itu pmb?', 'PMB adalah proses penerimaan mahasiswa baru di Politeknik Negeri Jakarta untuk berbagai program studi yang tersedia.', '2025-05-16 07:10:43', 0),
(7, 'kapan jadwal snbt pnj?', 'Jadwal SNBT di PNJ dimulai pada tanggal 11 sampai 27 Maret 2025.', '2025-05-16 16:50:13', 0),
(8, 'Berapa biaya pendaftaran Pascasarjana?', 'Biaya pendaftaran jalur Pascasarjana di PNJ adalah Rp500.000.', '2025-05-16 17:06:09', 0),
(9, 'berapa biaya pendaftaran jalur rpl?', 'Biaya pendaftaran jalur RPL di PNJ adalah Rp350.000.', '2025-05-16 17:07:00', 0),
(10, 'biaya pendaftaran pascasarjana berapa?', 'Biaya pendaftaran pascasarjana di PNJ adalah Rp500.000.', '2025-05-16 17:19:40', 0),
(11, 'kapan jadwal pendaftaran rpl?', 'Informasi tidak tersedia.', '2025-05-17 09:56:22', 0),
(12, 'kapan jadwal pendaftaran rpl?', 'Informasi tidak tersedia.', '2025-05-17 10:20:37', 0),
(13, 'kapan jadwal pendaftaran rpl?', 'Jadwal pendaftaran RPL dimulai pada tanggal 10 Juni – 19 Juli 2024.', '2025-05-17 10:23:35', 0),
(14, 'kapan jadwal pendaftaran rpl?', 'Jadwal pendaftaran RPL dimulai pada tanggal 10 Juni – 19 Juli 2024.', '2025-05-17 10:30:32', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `faq_final`
--
ALTER TABLE `faq_final`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `faq_suggestions`
--
ALTER TABLE `faq_suggestions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `faq_suggestion_variants`
--
ALTER TABLE `faq_suggestion_variants`
  ADD PRIMARY KEY (`id`),
  ADD KEY `suggestion_id` (`suggestion_id`);

--
-- Indexes for table `qa_data`
--
ALTER TABLE `qa_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `uploaded_files`
--
ALTER TABLE `uploaded_files`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_questions`
--
ALTER TABLE `user_questions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `faq_final`
--
ALTER TABLE `faq_final`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `faq_suggestions`
--
ALTER TABLE `faq_suggestions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `faq_suggestion_variants`
--
ALTER TABLE `faq_suggestion_variants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `qa_data`
--
ALTER TABLE `qa_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=173;

--
-- AUTO_INCREMENT for table `uploaded_files`
--
ALTER TABLE `uploaded_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user_questions`
--
ALTER TABLE `user_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `faq_suggestion_variants`
--
ALTER TABLE `faq_suggestion_variants`
  ADD CONSTRAINT `faq_suggestion_variants_ibfk_1` FOREIGN KEY (`suggestion_id`) REFERENCES `faq_suggestions` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
