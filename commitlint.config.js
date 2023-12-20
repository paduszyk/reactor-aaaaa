/**
 * Commitlint
 * https://commitlint.js.org/#/reference-configuration
 */

const Configuration = {
  extends: ["@commitlint/config-conventional"],
  ignores: [
    (message) => /[A-Z].*\s\(#\d+\)\n?/.test(message),
  ],
};

module.exports = Configuration;
