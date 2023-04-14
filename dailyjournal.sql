

CREATE TABLE `Entry` (
	`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
    `mood_id`   INTEGER NOT NULL,
    `date`  DATE NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
	`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);

CREATE TABLE `Tag` (
	`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`subject`	TEXT NOT NULL
);

CREATE TABLE `Entry_Tag` (
	`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`entry_id`	INTEGER NOT NULL,
    `tag_id`	INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);


INSERT INTO `Entry` VALUES (null, 'Javascript', "I learned about loops today. They can be a lot of fun. I learned about loops today. They can be a lot of fun. I learned about loops today. They can be a lot of fun.", 1, "2021-09-15");
INSERT INTO `Entry` VALUES (null, 'Python', "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake.", 4, "2021-09-15");
INSERT INTO `Entry` VALUES (null, 'Python', "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks.", 3, "2021-09-15");
INSERT INTO `Entry` VALUES (null, 'Javascript', "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, "2021-09-15");

INSERT INTO `Mood` VALUES (null, 'Happy');
INSERT INTO `Mood` VALUES (null, 'Sad');
INSERT INTO `Mood` VALUES (null, 'Angry');
INSERT INTO `Mood` VALUES (null, 'Ok');

INSERT INTO `Tag` VALUES (null, 'API');
INSERT INTO `Tag` VALUES (null, 'components');
INSERT INTO `Tag` VALUES (null, 'fetch');

INSERT INTO `Entry_tag` VALUES (null, 4, 2);
INSERT INTO `Entry_tag` VALUES (null, 4, 3);
INSERT INTO `Entry_tag` VALUES (null, 9, 1);
INSERT INTO `Entry_tag` VALUES (null, 9, 2);



DROP TABLE `Entry`;

CREATE TABLE `Entry` (
	`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
    `mood_id`   INTEGER NOT NULL,
    `date`  DATE NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

INSERT INTO `Entry` VALUES (null, 'Javascript', "I learned about loops today. They can be a lot of fun. I learned about loops today. They can be a lot of fun. I learned about loops today. They can be a lot of fun.", 1, "2021-09-15");
INSERT INTO `Entry` VALUES (null, 'Python', "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake.", 4, "2021-09-15");
INSERT INTO `Entry` VALUES (null, 'Python', "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks.", 3, "2021-09-15");
INSERT INTO `Entry` VALUES (null, 'Javascript', "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, "2021-09-15");