import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import fs from 'fs/promises';
import path from 'path';

export function createExampleAction() {
  return createTemplateAction({
    id: 'my:custom:action',
    description: 'Creates a new file in the temporary workspace',
    schema: {},
    async handler(ctx) {
      const filePath = path.join(ctx.workspacePath, 'custom-action-file.txt');

      await fs.writeFile(
        filePath,
        'This file was created by my:custom:action',
        'utf8',
      );

      ctx.logger.info(`Created file at ${filePath}`);
    },
  });
}