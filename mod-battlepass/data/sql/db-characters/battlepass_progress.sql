-- mod-battlepass v4: Fortschritt pro Charakter.
-- VOLLSTÄNDIG IDEMPOTENT: kann beliebig oft laufen (Auto-Updater-sicher).
-- Deckt Neuinstallation UND Upgrade von v1/v2/v3 ab — keine manuelle Migration nötig.

CREATE TABLE IF NOT EXISTS `character_battlepass` (
  `guid` INT UNSIGNED NOT NULL,
  `season` INT UNSIGNED NOT NULL DEFAULT 1,
  `points` INT UNSIGNED NOT NULL DEFAULT 0,
  `claimed_tier` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `claimed_epic` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `last_daily` INT UNSIGNED NOT NULL DEFAULT 0,
  `streak` INT UNSIGNED NOT NULL DEFAULT 0,
  `prestige` INT UNSIGNED NOT NULL DEFAULT 0,
  `xprate` INT UNSIGNED NOT NULL DEFAULT 100,
  `lang` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=Deutsch,1=Englisch',
  `chest_pity` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Kistenfieber',
  `welcomed` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Willkommenspaket erhalten',
  `hardcore` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=aus,1=aktiv,2=gescheitert,3=geschafft',
  `supply_day` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'letzter Versorgungsauftrag',
  `start_rune` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'gewaehlte Startfaehigkeit',
  `fish_day` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Tag des Angelauftrags',
  `fish_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'heutige Faenge',
  PRIMARY KEY (`guid`,`season`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Upgrade-Pfad: fehlende Spalten aus aelteren Versionen nachziehen.
-- (ADD COLUMN nur, wenn die Spalte fehlt — laeuft auf MySQL UND MariaDB.)
SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `claimed_epic` SMALLINT UNSIGNED NOT NULL DEFAULT 0 AFTER `claimed_tier`',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'claimed_epic');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `streak` INT UNSIGNED NOT NULL DEFAULT 0',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'streak');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `prestige` INT UNSIGNED NOT NULL DEFAULT 0',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'prestige');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `xprate` INT UNSIGNED NOT NULL DEFAULT 100',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'xprate');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `lang` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''0=Deutsch,1=Englisch''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'lang');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `chest_pity` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''Kistenfieber''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'chest_pity');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `welcomed` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''Willkommenspaket erhalten''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'welcomed');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `hardcore` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''0=aus,1=aktiv,2=gescheitert,3=geschafft''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'hardcore');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `supply_day` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''letzter Versorgungsauftrag''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'supply_day');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `start_rune` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''gewaehlte Startfaehigkeit''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'start_rune');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `fish_day` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''Tag des Angelauftrags''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'fish_day');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

SET @sql = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `character_battlepass` ADD COLUMN `fish_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT ''heutige Faenge''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'character_battlepass' AND COLUMN_NAME = 'fish_count');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- Wochenziele pro Charakter (Slots 0-2, Slot 8 = Traumtausch, Slot 9 = Dungeon der Woche)
CREATE TABLE IF NOT EXISTS `character_battlepass_weekly` (
  `guid` INT UNSIGNED NOT NULL,
  `week` INT UNSIGNED NOT NULL,
  `slot` TINYINT UNSIGNED NOT NULL,
  `challenge` INT UNSIGNED NOT NULL,
  `progress` INT UNSIGNED NOT NULL DEFAULT 0,
  `done` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`guid`,`week`,`slot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Aktive Runen pro Charakter
CREATE TABLE IF NOT EXISTS `character_battlepass_runes` (
  `guid` INT UNSIGNED NOT NULL,
  `rune` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`guid`,`rune`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Saison-Erfolge pro Charakter
CREATE TABLE IF NOT EXISTS `character_battlepass_ach` (
  `guid` INT UNSIGNED NOT NULL,
  `ach` INT UNSIGNED NOT NULL,
  `progress` INT UNSIGNED NOT NULL DEFAULT 0,
  `done` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`guid`,`ach`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Entdeckte verlorene Orte pro Charakter
CREATE TABLE IF NOT EXISTS `character_battlepass_discoveries` (
  `guid` INT UNSIGNED NOT NULL,
  `zone` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`guid`,`zone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
