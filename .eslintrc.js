// eslint-disable-next-line no-undef
module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
  },
  'extends': [
    'eslint:recommended',
    'plugin:react/recommended',
  ],
  'parserOptions': {
    'ecmaFeatures': {
      'jsx': true,
    },
    'ecmaVersion': 12,
    'sourceType': 'module',
  },
  'plugins': [
    'react',
    'react-hooks',
  ],
  'rules': {
    'indent': [
      'error',
      2,
      { 'SwitchCase': 1 },
    ],
    'quotes': [
      'error',
      'single',
    ],
    'semi': [
      'error',
      'always',
    ],
    'comma-dangle': [
      'error',
      'always-multiline',
    ],
    'prefer-const': [
      'error',
      {
        'destructuring': 'any',
        ignoreReadBeforeAssign: true,
      },
    ],
    'no-var':'error',
    'no-lonely-if': 'error',
    'no-duplicate-imports': [
      'error',
      { 'includeExports': true },
    ],
    'object-curly-spacing': [
      'error',
      'always',
      {
        'objectsInObjects': false,
        'arraysInObjects': false,
      },
    ],
    'jsx-quotes': [
      'error',
      'prefer-double',
    ],
    'arrow-spacing': [
      'error',
      { before: true, after: true },
    ],
    'prefer-destructuring': [
      'error',
      {
        VariableDeclarator: {
          array: false,
          object: true,
        },
        AssignmentExpression: {
          array: true,
          object: false,
        },
      },
      {
        enforceForRenamedProperties: false,
      },
    ],
    'react/jsx-filename-extension': [
      1,
      { 'allow': 'as-needed' },
    ],
    'react/jsx-uses-vars': 'error',
    'react/prop-types': 0,
    'react/jsx-tag-spacing': [
      'error',
      {
        beforeSelfClosing: 'always',
        afterOpening: 'never',
        closingSlash: 'never',
        beforeClosing: 'never',
      },
    ],
    'react-hooks/rules-of-hooks': 'error', // Checks rules of Hooks
    'react-hooks/exhaustive-deps': 'warn', // Checks effect dependencies
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
