-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-10-2017 a las 20:08:13
-- Versión del servidor: 10.1.21-MariaDB
-- Versión de PHP: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_holoeasy`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calculo_oid`
--

CREATE TABLE `calculo_oid` (
  `idcalculo_oid` int(11) NOT NULL,
  `masiroid` float DEFAULT NULL,
  `s1` int(11) DEFAULT NULL,
  `s2` int(11) DEFAULT NULL,
  `id_holograma` int(11) NOT NULL,
  `masirREF` float DEFAULT NULL,
  `optimiserODD` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `correo`
--

CREATE TABLE `correo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `mensaje` text COLLATE utf8_unicode_ci NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Esta tabla almacenara los correos enviados';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `holograma`
--

CREATE TABLE `holograma` (
  `idholograma` int(11) NOT NULL,
  `codigo` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `holograma_analogico`
--

CREATE TABLE `holograma_analogico` (
  `idholograma_analogico` int(11) NOT NULL,
  `id_holograma` int(11) NOT NULL,
  `sg_ilum` int(11) NOT NULL DEFAULT '2',
  `tipo_ilum` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `optimiser` tinyint(1) DEFAULT '1',
  `p1` int(11) DEFAULT '0',
  `p2` int(11) DEFAULT '0',
  `q1` int(11) DEFAULT '0',
  `q2` int(11) DEFAULT '0',
  `b1` int(11) DEFAULT '0',
  `b2` int(11) DEFAULT '0',
  `erreura` float DEFAULT NULL,
  `EDa` float DEFAULT NULL,
  `RSBa` float DEFAULT NULL,
  `uniforma` float DEFAULT NULL,
  `zerobruita` float DEFAULT NULL,
  `deviationstda` float DEFAULT NULL,
  `M` float DEFAULT NULL,
  `EA` float DEFAULT NULL,
  `UA` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `holograma_cuantificado`
--

CREATE TABLE `holograma_cuantificado` (
  `idholograma_cuantificado` int(11) NOT NULL,
  `erreurq` float DEFAULT NULL,
  `EDq` float DEFAULT NULL,
  `RSBq` float DEFAULT NULL,
  `uniformq` float DEFAULT NULL,
  `zerobruitq` float DEFAULT NULL,
  `deviationstdq` float DEFAULT NULL,
  `EQ` float DEFAULT NULL,
  `UQ` float DEFAULT NULL,
  `id_holograma` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros_regulacion`
--

CREATE TABLE `parametros_regulacion` (
  `id` int(11) NOT NULL,
  `id_holograma` int(11) NOT NULL,
  `analogo_iteraccion` int(11) NOT NULL DEFAULT '20',
  `analogo_PRs` float NOT NULL DEFAULT '1',
  `analogo_PRb` float NOT NULL DEFAULT '0',
  `analogo_DPRA` float NOT NULL DEFAULT '1',
  `analogo_DPLRA` float NOT NULL DEFAULT '0',
  `cuantificar_iteraccion` int(11) NOT NULL DEFAULT '20',
  `cuantificar_PRs` float NOT NULL DEFAULT '1',
  `cuantificar_PRb` float NOT NULL DEFAULT '0',
  `cuantificar_DPRA` float NOT NULL DEFAULT '1',
  `cuantificar_DPLRA` float NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `senal_reconstruir`
--

CREATE TABLE `senal_reconstruir` (
  `idsenal_reconstruir` int(11) NOT NULL,
  `id_holograma` int(11) NOT NULL,
  `tam_img` int(11) NOT NULL,
  `tam_x` int(11) DEFAULT NULL,
  `tam_y` int(11) DEFAULT NULL,
  `tam_obj` int(11) NOT NULL,
  `tam_obj_x` int(11) DEFAULT NULL,
  `tam_obj_y` int(11) DEFAULT NULL,
  `r1x` int(11) DEFAULT NULL,
  `r1y` int(11) DEFAULT NULL,
  `r2x` int(11) DEFAULT NULL,
  `r2y` int(11) DEFAULT NULL,
  `fase` varchar(45) COLLATE utf8_unicode_ci DEFAULT 'phaheur',
  `fase_inicial` varchar(45) COLLATE utf8_unicode_ci DEFAULT 'bandelimitee',
  `iteraccion` int(11) DEFAULT '20',
  `control_banda` float DEFAULT '0.01',
  `diffphase` float DEFAULT '1.335',
  `DPE` tinyint(4) DEFAULT '0',
  `nivel` int(11) DEFAULT '4',
  `MASIRdes` float DEFAULT '0.8',
  `tipoilum` varchar(45) COLLATE utf8_unicode_ci DEFAULT 'carre',
  `pixelmargin` int(11) DEFAULT '0',
  `taillesignal` int(11) DEFAULT '128',
  `tailleholo` int(11) DEFAULT '64',
  `tailleobject` int(11) NOT NULL,
  `code` varchar(45) COLLATE utf8_unicode_ci DEFAULT 'codedoux' COMMENT 'codedoux\ncodedur',
  `lissage2` float DEFAULT '0.8',
  `iteropt` int(11) DEFAULT '50',
  `iterODD` int(11) DEFAULT '100',
  `cuantificar` varchar(2) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'SI'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idusuario` int(11) NOT NULL,
  `tipo` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `usuario` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nombre` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apellido` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `calculo_oid`
--
ALTER TABLE `calculo_oid`
  ADD PRIMARY KEY (`idcalculo_oid`),
  ADD KEY `index_oid_holograma` (`id_holograma`);

--
-- Indices de la tabla `correo`
--
ALTER TABLE `correo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `holograma`
--
ALTER TABLE `holograma`
  ADD PRIMARY KEY (`idholograma`),
  ADD KEY `fk_holograma_usuario_idx` (`id_usuario`);

--
-- Indices de la tabla `holograma_analogico`
--
ALTER TABLE `holograma_analogico`
  ADD PRIMARY KEY (`idholograma_analogico`),
  ADD KEY `fk_analogico_holograma_idx` (`id_holograma`);

--
-- Indices de la tabla `holograma_cuantificado`
--
ALTER TABLE `holograma_cuantificado`
  ADD PRIMARY KEY (`idholograma_cuantificado`),
  ADD KEY `fk_cuantificado_holograma_idx` (`id_holograma`);

--
-- Indices de la tabla `parametros_regulacion`
--
ALTER TABLE `parametros_regulacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `holograma_id` (`id_holograma`);

--
-- Indices de la tabla `senal_reconstruir`
--
ALTER TABLE `senal_reconstruir`
  ADD PRIMARY KEY (`idsenal_reconstruir`),
  ADD KEY `fk_senal_holograma_idx` (`id_holograma`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idusuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `calculo_oid`
--
ALTER TABLE `calculo_oid`
  MODIFY `idcalculo_oid` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `correo`
--
ALTER TABLE `correo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `holograma`
--
ALTER TABLE `holograma`
  MODIFY `idholograma` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `holograma_analogico`
--
ALTER TABLE `holograma_analogico`
  MODIFY `idholograma_analogico` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `holograma_cuantificado`
--
ALTER TABLE `holograma_cuantificado`
  MODIFY `idholograma_cuantificado` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `parametros_regulacion`
--
ALTER TABLE `parametros_regulacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `senal_reconstruir`
--
ALTER TABLE `senal_reconstruir`
  MODIFY `idsenal_reconstruir` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idusuario` int(11) NOT NULL AUTO_INCREMENT;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `calculo_oid`
--
ALTER TABLE `calculo_oid`
  ADD CONSTRAINT `fk_holograma_oid` FOREIGN KEY (`id_holograma`) REFERENCES `holograma` (`idholograma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `holograma`
--
ALTER TABLE `holograma`
  ADD CONSTRAINT `fk_holograma_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`idusuario`);

--
-- Filtros para la tabla `holograma_analogico`
--
ALTER TABLE `holograma_analogico`
  ADD CONSTRAINT `fk_analogico_holograma` FOREIGN KEY (`id_holograma`) REFERENCES `holograma` (`idholograma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `holograma_cuantificado`
--
ALTER TABLE `holograma_cuantificado`
  ADD CONSTRAINT `fk_cuantificado_holograma` FOREIGN KEY (`id_holograma`) REFERENCES `holograma` (`idholograma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `parametros_regulacion`
--
ALTER TABLE `parametros_regulacion`
  ADD CONSTRAINT `parametros_regulacion_ibfk_1` FOREIGN KEY (`id_holograma`) REFERENCES `holograma` (`idholograma`);

--
-- Filtros para la tabla `senal_reconstruir`
--
ALTER TABLE `senal_reconstruir`
  ADD CONSTRAINT `fk_senal_holograma` FOREIGN KEY (`id_holograma`) REFERENCES `holograma` (`idholograma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
